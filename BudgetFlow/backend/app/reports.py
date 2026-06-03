from datetime import date

from sqlalchemy.orm import Session

from app.models import TransactionDB


def get_summary_report(
    db: Session,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    query = db.query(TransactionDB)

    if category is not None:
        query = query.filter(TransactionDB.category.ilike(category))

    if start_date is not None:
        query = query.filter(TransactionDB.transaction_date >= start_date)

    if end_date is not None:
        query = query.filter(TransactionDB.transaction_date <= end_date)

    results = query.all()

    total_spending = sum(transaction.amount for transaction in results)
    transaction_count = len(results)

    if transaction_count > 0:
        average_spending = round(total_spending / transaction_count, 2)
    else:
        average_spending = 0

    spending_by_category = {}

    for transaction in results:
        category_name = transaction.category

        if category_name not in spending_by_category:
            spending_by_category[category_name] = 0

        spending_by_category[category_name] += transaction.amount

    response = {
        "category": category,
        "start_date": start_date,
        "end_date": end_date,
        "total_spending": total_spending,
        "transaction_count": transaction_count,
        "average_spending": average_spending,
    }

    if category is None:
        response["spending_by_category"] = spending_by_category

    return response


def get_monthly_report(
    db: Session,
    category: str | None = None
):
    query = db.query(TransactionDB)

    if category is not None:
        query = query.filter(TransactionDB.category.ilike(category))

    results = query.all()

    monthly_spending = {}

    for transaction in results:
        month_key = transaction.transaction_date.strftime("%Y-%m")

        if month_key not in monthly_spending:
            monthly_spending[month_key] = 0

        monthly_spending[month_key] += transaction.amount

    for month in monthly_spending:
        monthly_spending[month] = round(monthly_spending[month], 2)

    return {
        "category": category,
        "monthly_spending": monthly_spending
    }