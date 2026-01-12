from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional

from pdf_ingestor import PDFIngestor
from pdf_transaction_extractor import PDFTransactionExtractor
from transaction_parser import TransactionParser
from pipeline import ExpenseCategorizationPipeline
from bulk_processor import BulkExpenseProcessor
from analytics_engine import AnalyticsEngine

router = APIRouter(
    prefix="/pdf",
    tags=["PDF Upload"]
)

# Initialize core components ONCE
pdf_ingestor = PDFIngestor()
txn_extractor = PDFTransactionExtractor()
parser = TransactionParser()

pipeline = ExpenseCategorizationPipeline(
    model_path="model.joblib",
    vectorizer_path="vectorizer.joblib"
)

bulk_processor = BulkExpenseProcessor(pipeline)


@router.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...),
    password: Optional[str] = Form(None)
):
    """Upload a bank statement PDF for analysis"""

    # 1️⃣ Save uploaded file temporarily
    pdf_path = f"temp_{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # 2️⃣ Extract text from PDF
    pdf_result = pdf_ingestor.extract_text(
        pdf_path=pdf_path,
        password=password
    )

    if not pdf_result["success"]:
        return {
            "status": "error",
            "message": pdf_result["error"]
        }

    # 3️⃣ Extract transaction lines
    transaction_lines = txn_extractor.extract_transactions(
        pdf_result["text"]
    )

    if not transaction_lines:
        return {
            "status": "error",
            "message": "No transaction lines found in PDF."
        }

    # 4️⃣ Parse transactions
    parsed_transactions = parser.parse(transaction_lines)

    if not parsed_transactions:
        return {
            "status": "error",
            "message": "No valid transactions parsed."
        }

    # 5️⃣ Categorize (bulk)
    categorized = bulk_processor.process_transactions(parsed_transactions)

    # 6️⃣ Analytics
    analytics = AnalyticsEngine(categorized)

    return {
        "status": "success",
        "transactions_count": len(categorized),
        "transactions": categorized,
        "analytics": analytics.summary(),
        
    }
