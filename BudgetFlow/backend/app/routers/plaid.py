from fastapi import APIRouter, HTTPException
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest

from app import config
from app.plaid_client import client
from app.schemas import PublicTokenExchangeRequest


router = APIRouter(
    prefix="/plaid",
    tags=["plaid"]
)


@router.post("/create-link-token")
def create_link_token():
    if not config.PLAID_CLIENT_ID or not config.PLAID_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Plaid credentials are not configured"
        )

    request = LinkTokenCreateRequest(
        products=[Products(config.PLAID_PRODUCTS)],
        client_name="BudgetFlow",
        country_codes=[CountryCode(config.PLAID_COUNTRY_CODES)],
        language="en",
        user=LinkTokenCreateRequestUser(
            client_user_id="demo-user"
        )
    )

    try:
        response = client.link_token_create(request)

        return {
            "link_token": response["link_token"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post("/exchange-public-token")
def exchange_public_token(request_body: PublicTokenExchangeRequest):
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=request_body.public_token
        )

        response = client.item_public_token_exchange(exchange_request)

        return {
            "access_token": response["access_token"],
            "item_id": response["item_id"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@router.post("/create-sandbox-public-token")
def create_sandbox_public_token():
    try:
        request = SandboxPublicTokenCreateRequest(
            institution_id="ins_109508",
            initial_products=[Products(config.PLAID_PRODUCTS)]
        )

        response = client.sandbox_public_token_create(request)

        return {
            "public_token": response["public_token"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )