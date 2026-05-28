from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date

app = FastAPI(
    title="BudgetFlow API",
    description="Backend API for the BudgetFlow personal finance dashboard.",
    version="0.1.0",
)

class TransactionCreate(BaseModel):
    # defines the structure of a new transaction being created
    name: str
    amount: float
    category: str
    transaction_date: date

class Transaction(TransactionCreate):
    # adds a unique id identifier to a new transaction
    id: int

transactions: list[Transaction] = [] # transactions will be a list stored in memory for now, but this can be replaced with a database in the future
next_transaction_id = 1 # counter for the next unique id to assign to a new transaction

@app.get("/")
def root():
    return {
        "message": "BudgetFlow API is running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/transactions", response_model=list[Transaction])
def get_transactions(
    category: str | None = None,        # Query Parameters for filtering transactions
    min_amount: float | None = None,    
    max_amount: float | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    results = transactions

    if category is not None:
        results = [
            transaction
            for transaction in results
            if transaction.category.lower() == category.lower()
        ]

    if min_amount is not None:
        results = [
            transaction
            for transaction in results
            if transaction.amount >= min_amount
        ]

    if max_amount is not None:
        results = [
            transaction
            for transaction in results
            if transaction.amount <= max_amount
        ]

    if start_date is not None:
        results = [
            transaction
            for transaction in results
            if transaction.transaction_date >= start_date
        ]

    if end_date is not None:
        results = [
            transaction
            for transaction in results
            if transaction.transaction_date <= end_date
        ]
    return results

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int):
    # Retrieve a transaction by its unique id using a path parameter

    # Divide and conquer search
    low = 0
    high = len(transactions) - 1

    while low <= high:
        mid = (low + high) // 2
        if transactions[mid].id == transaction_id:
            return transactions[mid]
        elif transactions[mid].id < transaction_id:
            low = mid + 1
        else:
            high = mid - 1

    # Transaction not found, raise a 404 error
    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )

@app.post("/transactions", response_model=Transaction)
def create_transaction(transaction: TransactionCreate):
    global next_transaction_id

    new_transaction = Transaction(
        id=next_transaction_id,
        name=transaction.name,
        amount=transaction.amount,
        category=transaction.category,
        transaction_date=transaction.transaction_date
    )

    transactions.append(new_transaction)

    # Sorting the transactions list is not needed for testing. Will use later when we switch to a database
    
    # Ensure transactions are always sorted by id after adding a new transaction
    # transactions.sort(key=lambda x: x.id)

    next_transaction_id += 1

    return new_transaction

@app.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, updated_transaction: TransactionCreate):
    
    # Divide and conquer search
    low = 0
    high = len(transactions) - 1

    while low <= high:
        mid = (low + high) // 2
        if transactions[mid].id == transaction_id:
            transactions[mid] = Transaction(
                id=transaction_id,
                name=updated_transaction.name,
                amount=updated_transaction.amount,
                category=updated_transaction.category,
                transaction_date=updated_transaction.transaction_date
            )

            return transactions[mid]

        if transactions[mid].id < transaction_id:
            low = mid + 1
        else:
            high = mid - 1

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    # delete a transaction by its unique id
    for transaction in transactions:
        if transaction.id == transaction_id:
            transactions.remove(transaction)
            return {
                "message": "Transaction deleted",
                "deleted_transaction_id": transaction_id
            }

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )