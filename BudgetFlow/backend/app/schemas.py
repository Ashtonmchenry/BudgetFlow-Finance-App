# API request/response models (API data shapes)

from datetime import date

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    name: str
    amount: float
    category: str
    transaction_date: date

# Does not include plaid_transaction_id which is fine.
# That column is for avoiding duplicates and not needed in the API response
class Transaction(TransactionCreate): 
    id: int

    class Config:
        from_attributes = True


class PublicTokenExchangeRequest(BaseModel):  # plaid schema
    public_token: str
