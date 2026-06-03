from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import TransactionDB
from app.schemas import Transaction, TransactionCreate


app = FastAPI(
    title="BudgetFlow API",
    description="Backend API for the BudgetFlow personal finance dashboard.",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "BudgetFlow API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/transactions", response_model=Transaction)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
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


@app.get("/transactions", response_model=list[Transaction])
def get_transactions(
    category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
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


@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = (
        db.query(TransactionDB)
        .filter(TransactionDB.id == transaction_id)
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


@app.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    transaction = (
        db.query(TransactionDB)
        .filter(TransactionDB.id == transaction_id)
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transaction.name = updated_transaction.name
    transaction.amount = updated_transaction.amount
    transaction.category = updated_transaction.category
    transaction.transaction_date = updated_transaction.transaction_date

    db.commit()
    db.refresh(transaction)

    return transaction


@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = (
        db.query(TransactionDB)
        .filter(TransactionDB.id == transaction_id)
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return {
        "message": "Transaction deleted",
        "deleted_transaction_id": transaction_id
    }


@app.get("/reports/summary")
def get_summary(
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(TransactionDB)

    if category is not None:
        query = query.filter(TransactionDB.category.ilike(category))

    if start_date is not None:
        query = query.filter(TransactionDB.transaction_date >= start_date)

    if end_date is not None:
        query = query.filter(TransactionDB.transaction_date <= end_date)

    results = query.all()

    total_spending = sum(transaction.amount for transaction in results)
    transaction_count = len(results)

    if transaction_count > 0:
        average_spending = round(total_spending / transaction_count, 2)
    else:
        average_spending = 0

    spending_by_category = {}

    for transaction in results:
        category_name = transaction.category

        if category_name not in spending_by_category:
            spending_by_category[category_name] = 0

        spending_by_category[category_name] += transaction.amount

    response = {
        "category": category,
        "start_date": start_date,
        "end_date": end_date,
        "total_spending": total_spending,
        "transaction_count": transaction_count,
        "average_spending": average_spending,
    }

    if category is None:
        response["spending_by_category"] = spending_by_category

    return response


@app.get("/reports/monthly")
def get_monthly_report(
    category: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(TransactionDB)

    if category is not None:
        query = query.filter(TransactionDB.category.ilike(category))

    results = query.all()

    monthly_spending = {}

    for transaction in results:
        month_key = transaction.transaction_date.strftime("%Y-%m")

        if month_key not in monthly_spending:
            monthly_spending[month_key] = 0

        monthly_spending[month_key] += transaction.amount

    for month in monthly_spending:
        monthly_spending[month] = round(monthly_spending[month], 2)

    return {
        "category": category,
        "monthly_spending": monthly_spending
    }