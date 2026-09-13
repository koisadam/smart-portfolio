from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Response
from schemas.transaction import TransactionCreate, TransactionPublic, TransactionUpdate
from api.dependencies import FilterParams
from services.transaction_srv import TransactionService
from schemas.user import User
from core.security import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TransactionPublic)
def add_transaction(transaction: TransactionCreate, service: Annotated[TransactionService, Depends()], user: Annotated[User, Depends(get_current_user)]):
    new_transaction = service.add_transaction(transaction, user)
    if not new_transaction:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return new_transaction

@router.get("/", response_model=list[TransactionPublic])
def get_transactions(filter: Annotated[FilterParams, Depends()], service: Annotated[TransactionService, Depends()], user: Annotated[User, Depends(get_current_user)], portfolio_id: int | None = None):
    return service.get_transactions(filter, user, portfolio_id)

@router.get("/{transaction_id}", response_model=TransactionPublic)
def get_transaction(transaction_id: int, service: Annotated[TransactionService, Depends()], user: Annotated[User, Depends(get_current_user)]):
    transaction = service.get_transaction(transaction_id, user)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.patch("/{transaction_id}", response_model=TransactionPublic)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, service: Annotated[TransactionService, Depends()], user: Annotated[User, Depends(get_current_user)]):
    db_transaction = service.update_transaction(transaction_id, transaction, user)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, service: Annotated[TransactionService, Depends()], user: Annotated[User, Depends(get_current_user)]):
    success = service.delete_transaction(transaction_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)