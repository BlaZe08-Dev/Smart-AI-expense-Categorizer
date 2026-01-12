from pdf_ingestor import PDFIngestor
from transactions_parser import TransactionParser

ingestor = PDFIngestor()
parser = TransactionParser()

pdf = ingestor.extract_text("demo_bank_statement.pdf")

if not pdf["success"]:
    print("❌ PDF ERROR:", pdf["error"])
else:
    txns = parser.parse(pdf["text"])
    print("✅ PARSED TRANSACTIONS:")
    for t in txns:
        print(t)
