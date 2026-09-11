from fastapi import APIRouter, HTTPException, Response, status
from schemas.portfolio import PortfolioCreate, Portfolio, PortfolioPublic, PortfolioUpdate, PortfolioWithTransactions
from database import SessionDependency
from dependencies import FilterParams
from sqlmodel import select

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_portfolio(session: SessionDependency, portfolio: PortfolioCreate) -> PortfolioPublic:
    new_portfolio = Portfolio.model_validate(portfolio)
    session.add(new_portfolio)
    session.commit()
    session.refresh(new_portfolio)
    return new_portfolio

@router.get("/")
def get_portfolios(session: SessionDependency, filter: FilterParams) -> list[PortfolioPublic]:
    return session.exec(select(Portfolio).offset(filter.offset).limit(filter.limit)).all()

@router.get("/{portfolio_id}")
def get_portfolio(session: SessionDependency, portfolio_id: int) -> PortfolioWithTransactions:
    portfolio = session.get(Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.patch("/{portfolio_id}")
def update_portfolio(session: SessionDependency, portfolio_id: int, portfolio: PortfolioUpdate) -> PortfolioPublic:
    db_portfolio = session.get(Portfolio, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    new_portfolio = portfolio.model_dump(exclude_unset=True)
    db_portfolio.sqlmodel_update(new_portfolio)
    session.commit()
    session.refresh(db_portfolio)
    return db_portfolio

@router.delete("/{portfolio_id}")
def delete_portfolio(session: SessionDependency, portfolio_id: int) -> Response:
    portfolio = session.get(Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    session.delete(portfolio)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)