from fastapi import APIRouter, Depends, HTTPException

from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest

from app import config, crud
from app.plaid_client import client
from app.schemas import PublicTokenExchangeRequest
from app.database import get_db

from sqlalchemy.orm import Session


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

# endpoint no longer exposes the access token in the response, but it still saves the access token in the database for testing
@router.post("/exchange-public-token")
def exchange_public_token(
    request_body: PublicTokenExchangeRequest,
    db: Session = Depends(get_db)
):
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=request_body.public_token
        )

        response = client.item_public_token_exchange(exchange_request)

        access_token = response["access_token"]
        item_id = response["item_id"]

        crud.create_plaid_item(
            db=db,
            item_id=item_id,
            access_token=access_token
        )

        return {
            "message": "Plaid item connected successfully",
            "item_id": item_id
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

# Temporary backend endpoint for testing Plaid integration without a frontend.
# This asks Plaid Sandbox to create a fake public_token.
# Then we can pass that public_token into POST /plaid/exchange-public-token.
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
    
@router.post("/sync-transactions")
def sync_transactions(db: Session = Depends(get_db)):
    plaid_item = crud.get_first_plaid_item(db)

    if plaid_item is None:
        raise HTTPException(
            status_code=404,
            detail="No Plaid item found. Exchange a public token first."
        )

    added_count = 0
    modified_count = 0
    removed_count = 0

    cursor = plaid_item.cursor
    has_more = True
    latest_cursor = cursor

    try:
        while has_more:
            if cursor is None: # the first sync, should not send a cursor at all
                request = TransactionsSyncRequest(
                access_token=plaid_item.access_token
            )
            else:
                request = TransactionsSyncRequest(
                    access_token=plaid_item.access_token,
                    cursor=cursor
                )

            response = client.transactions_sync(request)

            added_transactions = response["added"]
            modified_transactions = response["modified"]
            removed_transactions = response["removed"]

            for plaid_transaction in added_transactions:
                transaction_data = plaid_transaction.to_dict()

                transaction_id = transaction_data["transaction_id"]
                name = transaction_data["name"]
                amount = transaction_data["amount"]
                transaction_date = transaction_data["date"]

                personal_finance_category = transaction_data.get(
                    "personal_finance_category"
                )

                if personal_finance_category is not None:
                    category = personal_finance_category.get(
                        "primary",
                        "Uncategorized"
                    )
                else:
                    category = "Uncategorized"

                crud.create_transaction_from_plaid(
                    db=db,
                    plaid_transaction_id=transaction_id,
                    name=name,
                    amount=amount,
                    category=category,
                    transaction_date=transaction_date
                )

                added_count += 1

            modified_count += len(modified_transactions)
            removed_count += len(removed_transactions)

            latest_cursor = response["next_cursor"]
            cursor = latest_cursor
            has_more = response["has_more"]

        crud.update_plaid_item_cursor(
            db=db,
            plaid_item=plaid_item,
            cursor=latest_cursor
        )

        return {
            "message": "Transactions synced successfully",
            "added": added_count,
            "modified": modified_count,
            "removed": removed_count,
            "cursor_saved": bool(latest_cursor)
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )