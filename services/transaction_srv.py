from schemas.user import User
from schemas.transaction import TransactionCreate, Transaction, TransactionUpdate
from api.dependencies import SessionDependency, FilterParams
from sqlmodel import select, desc
from typing import Sequence
from schemas.portfolio import Portfolio

class TransactionService:
    def __init__(self, session: SessionDependency):
        self.session = session

    def add_transaction(self, transaction: TransactionCreate, user: User) -> Transaction | None:
        portfolio = self.session.get(Portfolio, transaction.portfolio_id)
        if not portfolio or portfolio.user_id != user.id:
            return None
        new_transaction = Transaction.model_validate(transaction)
        self.session.add(new_transaction)
        self.session.commit()
        self.session.refresh(new_transaction)
        return new_transaction

    def get_transactions(self, filter: FilterParams, user: User, portfolio_id: int | None = None) -> Sequence[Transaction]:
        query = select(Transaction).join(Portfolio).where(Portfolio.user_id == user.id)
        if portfolio_id:
            query = query.where(Transaction.portfolio_id == portfolio_id)
        return self.session.exec(query.order_by(desc(Transaction.created_at)).offset(filter.offset).limit(filter.limit)).all()

    def get_transaction(self, transaction_id: int, user: User) -> Transaction | None:
        transaction = self.session.get(Transaction, transaction_id)
        if not transaction or transaction.portfolio.user_id != user.id:
            return None
        return transaction

    def update_transaction(self, transaction_id: int, transaction: TransactionUpdate, user: User) -> Transaction | None:
        db_transaction = self.get_transaction(transaction_id, user)
        if not db_transaction:
            return None
        new_transaction = transaction.model_dump(exclude_unset=True)
        db_transaction.sqlmodel_update(new_transaction)
        self.session.commit()
        self.session.refresh(db_transaction)
        return db_transaction

    def delete_transaction(self, transaction_id: int, user: User) -> bool:
        transaction = self.get_transaction(transaction_id, user)
        if not transaction:
            return False
        self.session.delete(transaction)
        self.session.commit()
        return True