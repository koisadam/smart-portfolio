from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class UserBase(SQLModel):
    username: str = Field(index=True)
    email: EmailStr = Field(index=True)
    full_name: str | None = Field(default=None)

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field()
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})
    
class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None
    
class UserPublic(UserBase):
    id: int