from fastapi import APIRouter
from pydantic import BaseModel
from typing import List,Dict

from ..pipeline import ExpenseCategorizationPipeline
from ..bulk_processor import BulkExpenseProcessor
from ..analytics_engine import AnalyticsEngine
from .ingest_api import TRANSACTIONS_STORE

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

#Initialize Shared Pipeline
pipeline = ExpenseCategorizationPipeline(
    model_path= "model.joblib",
    vectorizer_path = "vectorizer.joblib"
)

bulk_processor = BulkExpenseProcessor(pipeline)

#Request Schema
class BulkTransactionsRequest(BaseModel):
    transactions: List[Dict]

#API Endpoints
@router.get("/summary")
def analytics_summary(request: BulkTransactionsRequest):
    """
    Full analytics summary (used for dashboards)
    """
    categorized = bulk_processor.process_transactions(request.transactions)
    analytics = AnalyticsEngine(categorized)

    return analytics.summary()

@router.post("/category")
def category_breakdown(request: BulkTransactionsRequest):
    """
    Category-wise spending totals
    """
    categorized = bulk_processor.process_transactions(request.transactions)
    analytics = AnalyticsEngine(categorized)

    return analytics.category_totals()

@router.post("/merchant")
def merchant_breakdown(request: BulkTransactionsRequest):
    """
    Merchant-wise spending totals
    """
    categorized = bulk_processor.process_transactions(request.transactions)
    analytics = AnalyticsEngine(categorized)

    return analytics.merchant_totals()

@router.post("/daily")
def daily_breakdown(request: BulkTransactionsRequest):
    """
    Daily spending totals
    """
    categorized = bulk_processor.process_transactions(request.transactions)
    analytics = AnalyticsEngine(categorized)

    return analytics.daily_totals()

@router.post("/monthly")
def monthly_breakdown(request: BulkTransactionsRequest):
    """
    Monthly spending totals
    """
    categorized = bulk_processor.process_transactions(request.transactions)
    analytics = AnalyticsEngine(categorized)

    return analytics.monthly_totals()

