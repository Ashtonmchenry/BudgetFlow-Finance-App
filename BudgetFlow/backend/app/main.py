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
def get_transactions():
    return transactions

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int):
    # retrieve a transaction by its unique id using a divide and conquer approach
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

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )

@app.post("/transactions", response_model=Transaction)
def create_transaction(transaction: TransactionCreate):
    global next_transaction_id # we need to declare this as global since we will be modifying it inside the function

    new_transaction = Transaction(
        id=next_transaction_id,
        name=transaction.name,
        amount=transaction.amount,
        category=transaction.category,
        transaction_date=transaction.transaction_date
    )

    transactions.append(new_transaction)

    # transactions.sort(key=lambda x: x.id) # ensure transactions are always sorted by id after adding a new transaction

    next_transaction_id += 1

    return new_transaction

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