from pydantic import BaseModel


class FilterParams(BaseModel):
    offset: int = 0
    limit: int = 10
