from fastapi import APIRouter, HTTPException, Response, status, Depends
from schemas.portfolio import PortfolioCreate, PortfolioPublic, PortfolioUpdate, PortfolioWithTransactions
from api.dependencies import FilterParams
from typing import Annotated
from services.portfolio_srv import PortfolioService
from schemas.user import User
from core.security import get_current_user

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PortfolioPublic)
def add_portfolio(portfolio: PortfolioCreate, service: Annotated[PortfolioService, Depends()], user: Annotated[User, Depends(get_current_user)]):
    return service.add_portfolio(portfolio, user)

@router.get("/", response_model=list[PortfolioPublic])
def get_portfolios(filter: Annotated[FilterParams, Depends()], service: Annotated[PortfolioService, Depends()], user: Annotated[User, Depends(get_current_user)]):
    return service.get_portfolios(filter, user)

@router.get("/{portfolio_id}", response_model=PortfolioWithTransactions)
def get_portfolio(portfolio_id: int, service: Annotated[PortfolioService, Depends()], user: Annotated[User, Depends(get_current_user)]):
    portfolio = service.get_portfolio(portfolio_id, user)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.patch("/{portfolio_id}", response_model=PortfolioPublic)
def update_portfolio(portfolio_id: int, portfolio: PortfolioUpdate, service: Annotated[PortfolioService, Depends()], user: Annotated[User, Depends(get_current_user)]):
    db_portfolio = service.update_portfolio(portfolio_id, portfolio, user)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_portfolio

@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_portfolio(portfolio_id: int, service: Annotated[PortfolioService, Depends()], user: Annotated[User, Depends(get_current_user)]):
    success = service.delete_portfolio(portfolio_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)