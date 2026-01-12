class TransactionModeDetector:
    def __init__(self):
        self.mode_rules = {
            "Subscription": [
                "auto debit",
                "monthly",
                "subscription",
                "autopay",
                "premium"
            ],
            "Utility": [
                "electricity",
                "water",
                "gas",
                "billpay",
                "recharge",
                "broadband",
                "wbsedcl",
                "bsnl",
                "airtel",
                "jio",
                "vi",
            ],
            "UPI": [
                "upi",
                "paytm",
                "gpay",
                "phonepe"
            ],
            "CARD": [
                "card",
                "debit",
                "credit",
                "visa",
                "mastercard",
                "rupay"
            ]
        }

        self.priority_order = [
            "Subscription",
            "Utility",
            "UPI",
            "CARD"
        ]

    def detect(self, normalized_text: str) -> dict:
        """
        Detect payment mode from normalized transaction text.
        """

        if not normalized_text:
            return self._unknown()


        for mode in self.priority_order:
            for keyword in self.mode_rules[mode]:
                if keyword in normalized_text:
                    return {
                        "mode": mode,
                        "confidence": self._confidence_for(mode)
                    }
        return self._unknown()
    
    def _confidence_for(self, mode: str) -> float:
        """
        Static confidence scores
        """

        return{
            "SUBSCRIPTION": 0.95,
            "UTILITY": 0.9,
            "UPI": 0.75,
            "CARD": 0.7
        }.get(mode, 0.0)
    
    def _unknown(self) -> dict:
        return {
            "moode": "UNKNOWN",
            "confidence": 0.0
        }
                