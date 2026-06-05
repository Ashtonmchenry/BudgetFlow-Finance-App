import plaid
from plaid.api import plaid_api
from plaid.api_client import ApiClient
from plaid.configuration import Configuration

from app import config


def get_plaid_environment():
    if config.PLAID_ENV == "sandbox":
        return plaid.Environment.Sandbox

    if config.PLAID_ENV == "development":
        return plaid.Environment.Development

    if config.PLAID_ENV == "production":
        return plaid.Environment.Production

    return plaid.Environment.Sandbox


configuration = Configuration(
    host=get_plaid_environment(),
    api_key={
        "clientId": config.PLAID_CLIENT_ID,
        "secret": config.PLAID_SECRET,
    },
)

api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)
