from pdf_ingestor import PDFIngestor
from transaction_parser import TransactionParser
from pipeline import ExpenseCategorizationPipeline
from bulk_processor import BulkExpenseProcessor

# Init components
ingestor = PDFIngestor()
parser = TransactionParser()

pipeline = ExpenseCategorizationPipeline(
    model_path="model.joblib",
    vectorizer_path="vectorizer.joblib"
)

bulk = BulkExpenseProcessor(pipeline)

# Step 1: PDF → text
pdf = ingestor.extract_text("demo_bank_statement.pdf")

if not pdf["success"]:
    print("❌ PDF ERROR:", pdf["error"])
    exit()

# Step 2: text → transactions
transactions = parser.parse(pdf["text"])

# Step 3: bulk categorize
results = bulk.process_transactions(transactions)

print("✅ BULK CATEGORIZATION RESULTS:\n")
for r in results:
    print(r)
