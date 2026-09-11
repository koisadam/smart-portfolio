from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Response
from schemas.transaction import TransactionCreate, TransactionPublic, TransactionUpdate
from api.dependencies import FilterParams
from services.transaction_srv import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TransactionPublic)
def add_transaction(transaction: TransactionCreate, service: Annotated[TransactionService, Depends()]):
    return service.add_transaction(transaction)

@router.get("/", response_model=list[TransactionPublic])
def get_transactions(filter: Annotated[FilterParams, Depends()], service: Annotated[TransactionService, Depends()], portfolio_id: int | None = None):
    return service.get_transactions(filter, portfolio_id)

@router.get("/{transaction_id}", response_model=TransactionPublic)
def get_transaction(transaction_id: int, service: Annotated[TransactionService, Depends()]):
    transaction = service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.patch("/{transaction_id}", response_model=TransactionPublic)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, service: Annotated[TransactionService, Depends()]):
    db_transaction = service.update_transaction(transaction_id, transaction)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, service: Annotated[TransactionService, Depends()]):
    success = service.delete_transaction(transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)