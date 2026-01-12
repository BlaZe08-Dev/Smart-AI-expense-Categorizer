from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from ..pipeline import ExpenseCategorizationPipeline

router = APIRouter(
    tags=["Categorization"]
)

pipeline = ExpenseCategorizationPipeline(
    model_path="model.joblib",
    vectorizer_path="vectorizer.joblib"
)

class TransactionRequest(BaseModel):
    raw_text: str
    amount: Optional[float] = None

class CategorizationResponse(BaseModel):
    category: Optional[str]
    confidence: Optional[float]
    source: str
    explanation: dict

@router.post("/categorize", response_model=CategorizationResponse)
def categorize_expense(request: TransactionRequest):
    return pipeline.process(
        raw_text=request.raw_text,
        amount=request.amount
    )
