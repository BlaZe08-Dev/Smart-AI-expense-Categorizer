class RuleBasedClassifier:
    """
    Deterministic merchant-based expense classification.
    """

    MERCHANT_CATEGORY_MAP = {
        # Food & Dining
        "ZOMATO": "FOOD",
        "SWIGGY": "FOOD",
        "DOMINOS": "FOOD",
        "PIZZA": "FOOD",

        # Groceries & Retail
        "RELIANCE": "GROCERIES",
        "DMART": "GROCERIES",
        "FLIPKART": "SHOPPING",
        "AMAZON": "SHOPPING",

        # Transport
        "UBER": "TRANSPORT",
        "OLA": "TRANSPORT",

        # Subscriptions
        "NETFLIX": "SUBSCRIPTIONS",
        "SPOTIFY": "SUBSCRIPTIONS",
        "YOUTUBE": "SUBSCRIPTIONS",

        # Utilities / Telecom
        "JIO": "UTILITIES",
        "AIRTEL": "UTILITIES",
        "VODAFONE": "UTILITIES",

        # Payments / Wallets
        "PAYTM": "WALLET",
        "PHONEPE": "WALLET",
        "GPAY": "WALLET",
    }

    def __init__(self, merchant_kb):
        self.merchant_kb = merchant_kb

    def classify(self, mode_result: dict, merchant_result: dict) -> dict:
        merchant = merchant_result.get("merchant")
        mode = mode_result.get("mode")

        if not merchant:
            return {"status": "NO_RULE"}

        merchant_upper = merchant.upper()

        # ---------------------------------
        # 1️⃣ Exact merchant rule
        # ---------------------------------
        if merchant_upper in self.MERCHANT_CATEGORY_MAP:
            return {
                "category": self.MERCHANT_CATEGORY_MAP[merchant_upper],
                "confidence": 1.0,
                "source": "RULE"
            }

        # ---------------------------------
        # 2️⃣ Partial keyword rule
        # ---------------------------------
        for key, category in self.MERCHANT_CATEGORY_MAP.items():
            if key in merchant_upper:
                return {
                    "category": category,
                    "confidence": 0.9,
                    "source": "RULE"
                }

        # ---------------------------------
        # 3️⃣ Mode-based fallback
        # ---------------------------------
        if mode == "UPI":
            return {
                "category": "TRANSFER",
                "confidence": 0.6,
                "source": "RULE"
            }

        # ---------------------------------
        # 4️⃣ No rule matched
        # ---------------------------------
        return {"status": "NO_RULE"}
