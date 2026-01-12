from fastapi import APIRouter
from typing import List,Dict

router = APIRouter(
    prefix="/ingest",
    tags=["Ingest"]
)

TRANSACTIONS_STORE: List[Dict] = []

@router.post("/ingest")
def ingest_transactions(transactions: List[Dict]):
    TRANSACTIONS_STORE.clear()
    TRANSACTIONS_STORE.extend(transactions)

    return{
        "status": "success",
        "count": len(TRANSACTIONS_STORE)
    }

@router.get("/")
def get_transactions():
    return{
        "transactions": TRANSACTIONS_STORE,
        "count": len(TRANSACTIONS_STORE)
    }