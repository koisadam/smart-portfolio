from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from enums.portfolio import PortfolioType, Currency
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas.transaction import Transaction, TransactionPublic

class PortfolioBase(SQLModel):
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    type: PortfolioType = Field(default=PortfolioType.MIXED)
    currency: Currency = Field(default=Currency.USD)
    is_active: bool = Field(default=True)

class Portfolio(PortfolioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})

    transactions: list["Transaction"] = Relationship(back_populates="portfolio", cascade_delete=True)

class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    type: PortfolioType | None = None
    currency: Currency | None = None
    is_active: bool | None = None


class PortfolioPublic(PortfolioBase):
    id: int
    created_at: datetime
    updated_at: datetime

class PortfolioWithTransactions(PortfolioPublic):
    transactions: list["TransactionPublic"] = []