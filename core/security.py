from schemas.token import TokenData
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
import jwt
from api.dependencies import SessionDependency
from sqlmodel import select
from schemas.user import User
from core.config import get_settings
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status
from schemas.user import User

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_by_username(username: str, session: SessionDependency):
    return session.exec(select(User).where(User.username == username)).first()

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def authenticate_user(username: str, password: str, session: SessionDependency) -> User | None:
    user = get_user_by_username(username, session)
    if not user:
        # Timing attack prevention
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: TokenData):
    to_encode = data.model_dump()
    expire = datetime.now(timezone.utc) + timedelta(minutes=get_settings().access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_settings().secret_key, algorithm=get_settings().algorithm)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDependency) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=[get_settings().algorithm])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(username, session)
    if not user:
        raise credentials_exception
    return user
    
