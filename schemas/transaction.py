from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas.portfolio import Portfolio

class TransactionBase(SQLModel):
    portfolio_id: int = Field(index=True, foreign_key="portfolio.id", ondelete="CASCADE")
    ticker: str = Field(index=True, max_length=20)
    quantity: float = Field(index=True, gt=0)
    price: float = Field(index=True)

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})
    portfolio: "Portfolio" = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(SQLModel):
    ticker: str | None = None
    quantity: float | None = None
    price: float | None = None


class TransactionPublic(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime