from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from core.database import engine

class FilterParams(BaseModel):
    offset: int = 0
    limit: int = 10

def get_session():
    with Session(engine) as session:
        yield session

SessionDependency = Annotated[Session, Depends(get_session)]