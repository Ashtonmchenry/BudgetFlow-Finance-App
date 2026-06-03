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