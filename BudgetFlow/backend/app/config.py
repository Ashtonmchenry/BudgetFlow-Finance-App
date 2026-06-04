import os

from dotenv import load_dotenv


load_dotenv() # load environment variables from .env file


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./budgetflow.db"
)