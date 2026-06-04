from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import Transaction, TransactionCreate


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"] # This tag is used for grouping endpoints on the API docs page
)


@router.post("", response_model=Transaction)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    return crud.create_transaction(
        db=db,
        transaction=transaction
    )


@router.get("", response_model=list[Transaction])
def get_transactions(
    category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_transactions(
        db=db,
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = crud.get_transaction_by_id(
        db=db,
        transaction_id=transaction_id
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    transaction = crud.update_transaction(
        db=db,
        transaction_id=transaction_id,
        updated_transaction=updated_transaction
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = crud.delete_transaction(
        db=db,
        transaction_id=transaction_id
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {
        "message": "Transaction deleted",
        "deleted_transaction_id": transaction_id
    }