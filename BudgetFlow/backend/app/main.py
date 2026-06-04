from fastapi import FastAPI

from app.database import Base, engine
from app.routers import reports, transactions


app = FastAPI(
    title="BudgetFlow API",
    description="Backend API for the BudgetFlow personal finance dashboard.",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(transactions.router)
app.include_router(reports.router)


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