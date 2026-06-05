# API request/response models (API data shapes)

from datetime import date

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    name: str
    amount: float
    category: str
    transaction_date: date


class Transaction(TransactionCreate):
    id: int

    class Config:
        from_attributes = True


class PublicTokenExchangeRequest(BaseModel):  # plaid schema
    public_token: str
