from fastapi import FastAPI

from app import config
from app.database import Base, engine
from app.routers import plaid, reports, transactions


app = FastAPI(
    title="BudgetFlow API",
    description="Backend API for the BudgetFlow personal finance dashboard.",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(transactions.router)
app.include_router(reports.router)
app.include_router(plaid.router)


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


@app.get("/config-check")
def config_check():
    return {
        "database_configured": bool(config.DATABASE_URL),
        "plaid_client_id_configured": bool(config.PLAID_CLIENT_ID),
        "plaid_secret_configured": bool(config.PLAID_SECRET),
        "plaid_env": config.PLAID_ENV,
        "plaid_products": config.PLAID_PRODUCTS,
        "plaid_country_codes": config.PLAID_COUNTRY_CODES
    }