from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import reports
from app.database import get_db


router = APIRouter(
    prefix="/reports",
    tags=["reports"] # This tag is used for grouping endpoints on the API docs page
)


@router.get("/summary")
def get_summary(
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    return reports.get_summary_report(
        db=db,
        category=category,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/monthly")
def get_monthly_report(
    category: str | None = None,
    db: Session = Depends(get_db)
):
    return reports.get_monthly_report(
        db=db,
        category=category
    )