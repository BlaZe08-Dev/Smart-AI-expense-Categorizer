from fastapi import APIRouter
from typing import List, Dict

from ..pipeline import ExpenseCategorizationPipeline
from ..bulk_processor import BulkExpenseProcessor
from .analytics_api import TRANSACTIONS_STORE

router = APIRouter(
    prefix="/bulk",
    tags=["Bulk Processing"]
)

pipeline = ExpenseCategorizationPipeline(
    model_path="model.joblib",
    vectorizer_path="vectorizer.joblib"
)

bulk_processor = BulkExpenseProcessor(pipeline)

@router.post("/categorize")
def bulk_categorize(transactions: List[Dict]):
    """
    Categorize multiple transactions and auto-ingest into analytics
    """
    results = bulk_processor.process_transactions(transactions)

    # Auto-ingest into analytics store
    TRANSACTIONS_STORE.clear()
    TRANSACTIONS_STORE.extend(results)

    return {
        "count": len(results),
        "transactions": results
    }
