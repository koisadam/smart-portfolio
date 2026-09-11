from fastapi import APIRouter, HTTPException, Response, status
from schemas.transaction import TransactionCreate, TransactionPublic, Transaction, TransactionUpdate
from database import SessionDependency
from dependencies import FilterParams
from sqlmodel import select

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_transaction(session: SessionDependency, transaction: TransactionCreate) -> TransactionPublic:
    new_transaction = Transaction.model_validate(transaction)
    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)
    return new_transaction

@router.get("/")
def get_transactions(session: SessionDependency, filter: FilterParams, portfolio_id: int | None = None) -> list[TransactionPublic]:
    query = select(Transaction)
    if portfolio_id:
        query = query.where(Transaction.portfolio_id == portfolio_id)
    return session.exec(query.offset(filter.offset).limit(filter.limit).order_by(Transaction.created_at.desc())).all()

@router.get("/{transaction_id}")
def get_transaction(session: SessionDependency, transaction_id: int) -> TransactionPublic:
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.patch("/{transaction_id}")
def update_transaction(session: SessionDependency, transaction_id: int, transaction: TransactionUpdate) -> TransactionPublic:
    db_transaction = session.get(Transaction, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    new_transaction = transaction.model_dump(exclude_unset=True)
    db_transaction.sqlmodel_update(new_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}")
def delete_transaction(session: SessionDependency, transaction_id: int) -> Response:
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
