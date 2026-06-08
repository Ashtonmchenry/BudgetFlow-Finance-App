# SQL table definitions

from sqlalchemy import Column, Date, Float, Integer, String

from app.database import Base


class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    transaction_date = Column(Date, nullable=False)

class PlaidItemDB(Base):
    __tablename__ = "plaid_items"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, nullable=False, unique=True, index=True)
    access_token = Column(String, nullable=False)