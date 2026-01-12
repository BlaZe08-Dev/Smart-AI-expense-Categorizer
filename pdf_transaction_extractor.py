import re
from typing import List, Dict


class PDFTransactionExtractor:
    """
    Extracts only transaction rows from raw PDF text.
    Designed for Indian bank statements (SBI-style).
    """

    DATE_PATTERN = re.compile(r"\b\d{2}-\d{2}-\d{2}\b")  # 12-10-25

    def extract_transactions(self, pdf_text: str) -> List[str]:
        """
        Input: full extracted PDF text
        Output: list of raw transaction lines (strings)
        """

        if not pdf_text:
            return []

        lines = pdf_text.splitlines()
        transactions = []

        in_transaction_section = False

        for line in lines:
            clean_line = line.strip()

            # Detect transaction table start
            if "TRANSACTION OVERVIEW" in clean_line.upper():
                in_transaction_section = True
                continue

            # Stop if footer or summary reached
            if in_transaction_section and (
                "RELATIONSHIP SUMMARY" in clean_line.upper()
                or "CLOSING BALANCE" in clean_line.upper()
                or "Visit https://" in clean_line
            ):
                break

            # Extract only rows that look like transactions
            if in_transaction_section and self._looks_like_transaction(clean_line):
                transactions.append(clean_line)

        return transactions

    def _looks_like_transaction(self, line: str) -> bool:
        """
        Heuristic check to identify transaction rows.
        """

        if not line:
            return False

        # Must contain a date
        if not self.DATE_PATTERN.search(line):
            return False

        # Must contain UPI / CARD / NEFT / IMPS etc.
        keywords = ["UPI", "CARD", "NEFT", "IMPS", "PAYTM", "GPAY", "GOOGLE", "AMAZON"]
        if not any(k in line.upper() for k in keywords):
            return False

        # Must contain a number (amount)
        if not re.search(r"\d+\.\d{2}", line):
            return False

        return True
