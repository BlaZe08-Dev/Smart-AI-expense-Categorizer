from typing import List, Dict
from .pipeline import ExpenseCategorizationPipeline


class BulkExpenseProcessor:
    """
    Processes multiple transactions using the stable V1 pipeline.
    """

    def __init__(self, pipeline: ExpenseCategorizationPipeline):
        self.pipeline = pipeline

    def process_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """
        Input: list of parsed transactions
        Output: list of categorized transactions
        """

        results = []

        for txn in transactions:
            try:
                raw_text = txn.get("raw_text")
                amount = txn.get("amount")

                if not raw_text or amount is None:
                    continue

                category_result = self.pipeline.process(
                    raw_text=raw_text,
                    amount=amount
                )

                results.append({
                    "date": txn.get("date"),
                    "raw_text": raw_text,
                    "amount": amount,
                    "type": txn.get("type", "debit"),
                    "category": category_result.get("category"),
                    "confidence": category_result.get("confidence"),
                    "source": category_result.get("source")
                })

            except Exception as e:
                print(f"[BulkProcessor] Skipped txn due to error: {e}")
            continue

        return results
