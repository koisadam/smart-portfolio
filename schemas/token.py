from sqlmodel import SQLModel, Field

class Token(SQLModel, table=True):
    access_token: str = Field()
    token_type: str = Field()

class TokenData(SQLModel):
    username: str | None = Field(default=None)