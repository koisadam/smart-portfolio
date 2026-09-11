from schemas.transaction import TransactionCreate, Transaction, TransactionUpdate
from api.dependencies import SessionDependency, FilterParams
from sqlmodel import select, desc
from typing import Sequence

class TransactionService:
    def __init__(self, session: SessionDependency):
        self.session = session

    def add_transaction(self, transaction: TransactionCreate) -> Transaction:
        new_transaction = Transaction.model_validate(transaction)
        self.session.add(new_transaction)
        self.session.commit()
        self.session.refresh(new_transaction)
        return new_transaction

    def get_transactions(self, filter: FilterParams, portfolio_id: int | None = None) -> Sequence[Transaction]:
        query = select(Transaction)
        if portfolio_id:
            query = query.where(Transaction.portfolio_id == portfolio_id)
        return self.session.exec(query.order_by(desc(Transaction.created_at)).offset(filter.offset).limit(filter.limit)).all()

    def get_transaction(self, transaction_id: int) -> Transaction | None:
        return self.session.get(Transaction, transaction_id)

    def update_transaction(self, transaction_id: int, transaction: TransactionUpdate) -> Transaction | None:
        db_transaction = self.session.get(Transaction, transaction_id)
        if not db_transaction:
            return None
        new_transaction = transaction.model_dump(exclude_unset=True)
        db_transaction.sqlmodel_update(new_transaction)
        self.session.commit()
        self.session.refresh(db_transaction)
        return db_transaction

    def delete_transaction(self, transaction_id: int) -> bool:
        transaction = self.session.get(Transaction, transaction_id)
        if not transaction:
            return False
        self.session.delete(transaction)
        self.session.commit()
        return True