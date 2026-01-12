from collections import defaultdict
from typing import List, Dict


class AnalyticsEngine:
    def __init__(self, transactions: List[Dict]):
        self.transactions = transactions or []

    def debit_summary(self):
        category_summary = defaultdict(float)

        for txn in self.transactions:
            category = txn.get("category") or "Others"
            if txn.get("type") == "debit":
                category_summary[category] += txn.get("amount", 0)

                return {
                    "category_summary": dict(category_summary),
                    "transactions_count": len(self.transactions)
                }

    # Category-wise total
    def category_totals(self) -> Dict[str, float]:
        totals = defaultdict(float)
        
        for txn in self.transactions:
            category = txn.get("category") or "Uncategorized"
            amount = txn.get("amount", 0.0)

            if txn.get("type") == "debit":
                totals[category] += amount

    
        return dict(totals)

    # Merchant-wise total
    def merchant_totals(self) -> Dict[str, float]:
        totals = defaultdict(float)

        for txn in self.transactions:
            merchant = txn.get("raw_text") or "Unknown"
            amount = txn.get("amount", 0.0)
            if txn.get("type") == "debit":
                totals[merchant] += amount

    
        return dict(totals)
    #Time_based totals (Daily ones)
    def daily_totals(self)-> Dict[str, float]:
        totals = defaultdict(float)

        for txn in self.transactions:
            date = txn.get("date")
            amount = txn.get("amount", 0.0)
            if txn.get("type") == "debit":
                totals[date] += amount

        return dict(totals)
    #Monthly Totals
    def monthly_totals(self) -> Dict[str, float]:
        totals = defaultdict(float)

        for txn in self.transactions:
            date = txn.get("date")
            amount = txn.get("amount", 0.0)
            if not date or txn.get("type") != "debit":
                continue

            #date format
            month_key = "/".join(date.split("/")[1:])
            totals[month_key] += amount

        return dict(totals)

    #Source Health(RULE VS AI)
    def source_health(self) -> Dict[str, int]:
        counts = defaultdict(int)

        for txn in self.transactions:
            source = txn.get("source", "UNKNOWN")
            counts[source] += 1
        return dict(counts)

    #Master Summary
    def summary(self) -> Dict:
        return {
        "category_totals": self.category_totals(),
        "merchant_totals": self.merchant_totals(),
        "daily_totals": self.daily_totals(),
        "monthly_totals": self.monthly_totals(),
        "source_health": self.source_health(),
        "total_spent": sum(
            txn.get("amount", 0.0)
            for txn in self.transactions
            if txn.get("type") == "debit"
        )
    }