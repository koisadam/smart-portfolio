from sqlalchemy.ext.asyncio import session
from api.dependencies import SessionDependency, FilterParams
from schemas.portfolio import PortfolioCreate, Portfolio, PortfolioUpdate
from sqlmodel import select
from typing import Sequence

class PortfolioService:
    def __init__(self, session: SessionDependency):
        self.session = session

    def add_portfolio(self, portfolio: PortfolioCreate) -> Portfolio:
        new_portfolio = Portfolio.model_validate(portfolio)
        self.session.add(new_portfolio)
        self.session.commit()
        self.session.refresh(new_portfolio)
        return new_portfolio

    def get_portfolios(self, filter: FilterParams) -> Sequence[Portfolio]:
        return self.session.exec(select(Portfolio).offset(filter.offset).limit(filter.limit)).all()

    def get_portfolio(self, portfolio_id: int) -> Portfolio | None:
        return self.session.get(Portfolio, portfolio_id)

    def update_portfolio(self, portfolio_id: int, portfolio: PortfolioUpdate) -> Portfolio | None:
        db_portfolio = self.session.get(Portfolio, portfolio_id)
        if not db_portfolio:
            return None
        new_portfolio = portfolio.model_dump(exclude_unset=True)
        db_portfolio.sqlmodel_update(new_portfolio)
        self.session.commit()
        self.session.refresh(db_portfolio)
        return db_portfolio

    def delete_portfolio(self, portfolio_id: int) -> bool:
        portfolio = self.session.get(Portfolio, portfolio_id)
        if not portfolio:
            return False
        self.session.delete(portfolio)
        self.session.commit()
        return True