from schemas.token import TokenData
from datetime import timedelta
from core.config import get_settings
from fastapi import APIRouter, Depends, HTTPException, status
from api.dependencies import SessionDependency
from schemas.token import Token
from core.security import authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter()

@router.post("/token", response_model=Token, tags=["auth"])
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDependency):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data=TokenData(sub=user.username))
    return Token(access_token=access_token, token_type="bearer")
    

    