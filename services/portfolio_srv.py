from sqlalchemy.ext.asyncio import session
from api.dependencies import SessionDependency, FilterParams
from schemas.portfolio import PortfolioCreate, Portfolio, PortfolioUpdate
from sqlmodel import select
from typing import Sequence
from schemas.user import User

class PortfolioService:
    def __init__(self, session: SessionDependency):
        self.session = session

    def add_portfolio(self, portfolio: PortfolioCreate, user: User) -> Portfolio:
        new_portfolio = Portfolio.model_validate(portfolio)
        new_portfolio.user_id = user.id
        self.session.add(new_portfolio)
        self.session.commit()
        self.session.refresh(new_portfolio)
        return new_portfolio

    def get_portfolios(self, filter: FilterParams, user: User) -> Sequence[Portfolio]:
        return self.session.exec(select(Portfolio).where(Portfolio.user_id == user.id).offset(filter.offset).limit(filter.limit)).all()

    def get_portfolio(self, portfolio_id: int, user: User) -> Portfolio | None:
        portfolio = self.session.get(Portfolio, portfolio_id)
        if not portfolio or portfolio.user_id != user.id:
            return None
        return portfolio

    def update_portfolio(self, portfolio_id: int, portfolio: PortfolioUpdate, user: User) -> Portfolio | None:
        db_portfolio = self.session.get(Portfolio, portfolio_id)
        if not db_portfolio or db_portfolio.user_id != user.id:
            return None
        new_portfolio = portfolio.model_dump(exclude_unset=True)
        db_portfolio.sqlmodel_update(new_portfolio)
        self.session.commit()
        self.session.refresh(db_portfolio)
        return db_portfolio

    def delete_portfolio(self, portfolio_id: int, user: User) -> bool:
        portfolio = self.session.get(Portfolio, portfolio_id)
        if not portfolio or portfolio.user_id != user.id:
            return False
        self.session.delete(portfolio)
        self.session.commit()
        return True