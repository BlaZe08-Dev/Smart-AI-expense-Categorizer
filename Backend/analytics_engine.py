from collections import defaultdict
from typing import List, Dict


class AnalyticsEngine:
    def __init__(self, transactions: List[Dict]):
        self.transactions = transactions or []

    # -----------------------------
    # CATEGORY TOTALS (DEBIT ONLY)
    # -----------------------------
    def category_totals(self) -> Dict[str, float]:
        totals = defaultdict(float)

        for txn in self.transactions:
            if txn.get("type") != "debit":
                continue

            category = txn.get("category") or "Others"
            totals[category] += txn.get("amount", 0.0)

        return dict(totals)

    # -----------------------------
    # MERCHANT TOTALS (DEBIT ONLY)
    # -----------------------------
    def merchant_totals(self) -> Dict[str, float]:
        totals = defaultdict(float)

        for txn in self.transactions:
            if txn.get("type") != "debit":
                continue

            merchant = txn.get("raw_text") or "Unknown"
            totals[merchant] += txn.get("amount", 0.0)

        return dict(totals)

    # -----------------------------
    # DAILY TOTALS (DEBIT ONLY)
    # -----------------------------
    def daily_totals(self) -> Dict[str, float]:
        totals = defaultdict(float)

        for txn in self.transactions:
            if txn.get("type") != "debit":
                continue

            date = txn.get("date")
            if not date:
                continue

            totals[date] += txn.get("amount", 0.0)

        return dict(totals)

    # -----------------------------
    # MONTHLY TOTALS (SAFE)
    # Supports: YYYY-MM-DD or DD-MM-YY
    # -----------------------------
    def monthly_totals(self) -> Dict[str, float]:
        totals = defaultdict(float)

        for txn in self.transactions:
            if txn.get("type") != "debit":
                continue

            date = txn.get("date")
            if not date:
                continue

            parts = date.split("-")
            if len(parts) == 3:
                # DD-MM-YY  OR  YYYY-MM-DD
                month_key = f"{parts[1]}-{parts[2]}"
                totals[month_key] += txn.get("amount", 0.0)

        return dict(totals)

    # -----------------------------
    # SOURCE HEALTH (RULE / AI / USER_OVERRIDE)
    # -----------------------------
    def source_health(self) -> Dict[str, int]:
        counts = defaultdict(int)

        for txn in self.transactions:
            source = txn.get("source", "UNKNOWN")
            counts[source] += 1

        return dict(counts)

    # -----------------------------
    # MASTER SUMMARY (USED BY FRONTEND)
    # -----------------------------
    def summary(self) -> Dict:
        debit_amounts = [
            txn.get("amount", 0.0)
            for txn in self.transactions
            if txn.get("type") == "debit"
        ]

        credit_amounts = [
            txn.get("amount", 0.0)
            for txn in self.transactions
            if txn.get("type") == "credit"
        ]

        daily = self.daily_totals()

        return {
            "category_totals": self.category_totals(),
            "merchant_totals": self.merchant_totals(),
            "daily_totals": daily,
            "monthly_totals": self.monthly_totals(),
            "source_health": self.source_health(),

            # 🔹 Financial Insights
            "total_spent": sum(debit_amounts),
            "total_credit": sum(credit_amounts),
            "total_debit": sum(debit_amounts),
            "daily_average_spent": (
                sum(debit_amounts) / max(len(daily), 1)
            ),
        }