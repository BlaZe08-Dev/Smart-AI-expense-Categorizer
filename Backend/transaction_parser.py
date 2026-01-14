import re
from typing import List, Dict, Optional


class TransactionParser:
    """
    Converts raw transaction lines into structured transaction dicts.
    Bank-statement safe parser.
    """

    DATE_PATTERN = re.compile(r"\b(\d{2}[-/]\d{2}[-/]\d{2,4} | \d{4}-\d{2})\b")
    AMOUNT_PATTERN = re.compile(r"(\d{1,3}(?:,\d{3})*(?:\.\d{2}))")

    def parse(self, transaction_lines: List[str]) -> List[Dict]:
        parsed = []

        for line in transaction_lines:
            try:
                if self._is_balance_line(line):
                    continue

                date = self._extract_date(line)
                txn_type = self._detect_type(line)
                amount = self._extract_amount(line)

                if not date or not amount or txn_type == "unknown":
                    continue

                parsed.append({
                    "date": date,
                    "raw_text": self._extract_description(line),
                    "amount": amount,
                    "type": txn_type
                })

            except Exception:
                continue

        return parsed

    # ---------- helpers ----------

    def _is_balance_line(self, line: str) -> bool:
        l = line.lower()
        return (
            "opening balance" in l
            or "closing balance" in l
            or ("balance" in l and "debit" not in l and "credit" not in l)
        )

    def _extract_date(self, line: str) -> Optional[str]:
        m = self.DATE_PATTERN.search(line)
        return m.group(0) if m else None

    def _detect_type(self, line: str) -> str:
        l = line.lower()
        if "debit" in l or "dr" in l:
            return "debit"
        if "credit" in l or "cr" in l:
            return "credit"
        return "unknown"

    def _extract_amount(self, line: str) -> Optional[float]:
        """
        Extract amount near debit/credit, ignore balances.
        """
        parts = re.split(r"\bdebit\b|\bcredit\b|\bdr\b|\bcr\b", line, flags=re.IGNORECASE)
        target = parts[-1] if len(parts) > 1 else line

        m = self.AMOUNT_PATTERN.search(target)
        if not m:
            return None

        try:
            return float(m.group(1).replace(",", ""))
        except ValueError:
            return None

    def _extract_description(self, line: str) -> str:
        """
        Extracts merchant / UPI / CARD description.
        Always returns a string.
        """
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            for p in parts:
                if p.upper().startswith(("UPI", "CARD", "NEFT", "IMPS")):
                    return p

        # fallback: remove date and amounts
        clean = self.DATE_PATTERN.sub("", line)
        clean = self.AMOUNT_PATTERN.sub("", clean)
        return clean.strip()
