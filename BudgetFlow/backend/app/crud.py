# database create/read/update/delete logic

from datetime import date

from sqlalchemy.orm import Session

from app.models import PlaidItemDB, TransactionDB
from app.schemas import TransactionCreate

def create_transaction(
    db: Session,
    transaction: TransactionCreate
):
    """Handles the database creation logic for creating a new transaction."""
    new_transaction = TransactionDB(
        name=transaction.name,
        amount=transaction.amount,
        category=transaction.category,
        transaction_date=transaction.transaction_date
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

def get_transactions(
    db: Session,
    category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    """Handles the filtered database query logic for retrieving transactions."""
    query = db.query(TransactionDB)

    if category is not None:
        query = query.filter(TransactionDB.category.ilike(category))

    if min_amount is not None:
        query = query.filter(TransactionDB.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(TransactionDB.amount <= max_amount)

    if start_date is not None:
        query = query.filter(TransactionDB.transaction_date >= start_date)

    if end_date is not None:
        query = query.filter(TransactionDB.transaction_date <= end_date)

    return query.order_by(TransactionDB.id).all()

def get_transaction_by_id(
    db: Session,
    transaction_id: int
):
    """Handles finding one transaction by its ID."""
    return (
        db.query(TransactionDB)
        .filter(TransactionDB.id == transaction_id)
        .first()
    )

def update_transaction(
    db: Session,
    transaction_id: int,
    updated_transaction: TransactionCreate
):
    """Handles updating one row in the transactions table."""
    transaction = get_transaction_by_id(db, transaction_id)

    if transaction is None:
        return None

    transaction.name = updated_transaction.name
    transaction.amount = updated_transaction.amount
    transaction.category = updated_transaction.category
    transaction.transaction_date = updated_transaction.transaction_date

    db.commit()
    db.refresh(transaction)

    return transaction

def delete_transaction(
    db: Session,
    transaction_id: int
):
    """Handles deleting one row from the transactions table."""
    transaction = get_transaction_by_id(db, transaction_id)

    if transaction is None:
        return None

    db.delete(transaction)
    db.commit()

    return transaction

def create_plaid_item(
    db: Session,
    item_id: str,
    access_token: str
):
    """Saves the Plaid access token in the SQLite database."""
    plaid_item = PlaidItemDB(
        item_id=item_id,
        access_token=access_token
    )

    db.add(plaid_item)
    db.commit()
    db.refresh(plaid_item)

    return plaid_item

def get_first_plaid_item(db: Session):
    return db.query(PlaidItemDB).first()

def update_plaid_item_cursor(
    db: Session,
    plaid_item: PlaidItemDB,
    cursor: str
):
    plaid_item.cursor = cursor
    db.commit()
    db.refresh(plaid_item)

    return plaid_item

def create_transaction_from_plaid(
    db: Session,
    plaid_transaction_id: str,
    name: str,
    amount: float,
    category: str,
    transaction_date
):
    existing_transaction = (
        db.query(TransactionDB)
        .filter(TransactionDB.plaid_transaction_id == plaid_transaction_id)
        .first()
    )

    if existing_transaction is not None:
        return existing_transaction

    new_transaction = TransactionDB(
        plaid_transaction_id=plaid_transaction_id,
        name=name,
        amount=amount,
        category=category,
        transaction_date=transaction_date
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction