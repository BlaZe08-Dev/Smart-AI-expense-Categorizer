from pdf_ingestor import PDFIngestor
from transaction_parser import TransactionParser
from pipeline import ExpenseCategorizationPipeline
from bulk_processor import BulkExpenseProcessor
from analytics_engine import AnalyticsEngine

# Initialize pipeline
pipeline = ExpenseCategorizationPipeline(
    model_path="model.joblib",
    vectorizer_path="vectorizer.joblib"
)

bulk = BulkExpenseProcessor(pipeline)
parser = TransactionParser()
ingestor = PDFIngestor()

# PDF → text
pdf = ingestor.extract_text("demo_bank_statement.pdf")
transactions = parser.parse(pdf["text"])

# Bulk categorize
categorized = bulk.process_transactions(transactions)

# Analytics
analytics = AnalyticsEngine(categorized)
summary = analytics.summary()

print("\n📊 ANALYTICS SUMMARY\n")
for k, v in summary.items():
    print(f"{k}: {v}")
