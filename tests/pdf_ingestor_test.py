from pdf_ingestor import PDFIngestor

ingestor = PDFIngestor()

result = ingestor.extract_text(
    pdf_path="demo_bank_statement.pdf",
    password="YOUR_PASSWORD_IF_ANY"
)

if result["success"]:
    print("✅ PDF TEXT EXTRACTED")
    print(result["text"][:500])  # print first 500 chars
else:
    print("❌ ERROR:", result["error"])
