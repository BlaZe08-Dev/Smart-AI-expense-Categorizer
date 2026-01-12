from typing import Optional, Dict
import pdfplumber


class PDFIngestor:
    """
    Handles PDF → text extraction.
    Supports password-protected bank statements.
    """

    def extract_text(
        self,
        pdf_path: str,
        password: Optional[str] = None
    ) -> Dict:
        """
        Extracts text from a PDF file.

        Returns:
        {
            "success": bool,
            "text": str | None,
            "error": str | None
        }
        """

        try:
            with pdfplumber.open(pdf_path, password=password) as pdf:
                full_text = []

                for page_number, page in enumerate(pdf.pages, start=1):
                    try:
                        page_text = page.extract_text() or ""
                        full_text.append(page_text)
                    except Exception:
                        # Skip unreadable page, continue safely
                        continue

                combined_text = "\n".join(full_text).strip()

                if not combined_text:
                    return {
                        "success": False,
                        "text": None,
                        "error": "No readable text found in PDF"
                    }

                return {
                    "success": True,
                    "text": combined_text,
                    "error": None
                }

        except Exception as e:
            return {
                "success": False,
                "text": None,
                "error": f"PDF extraction failed: {str(e)}"
            }
