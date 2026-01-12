class MerchantKnowledgeBase:
    """
    Lightweight merchant intelligence layer. Stores Merchant -> Category mapping with confidence
    """

    def __init__(self):
        # Normalized merchant keyword → category
        self.merchant_category_map = {
            # Food & drinks
            "TEA": "Food",
            "TEASHOP": "Food",
            "SWEET": "Food",
            "SWEETSHOP": "Food",
            "RESTAURANT": "Food",
            "CAFE": "Food",

            # Groceries
            "VEGETABLE": "Groceries",
            "VEG": "Groceries",
            "GROCERY": "Groceries",
            "MARKET": "Groceries",

            # Transport
            "BUS": "Transport",
            "BUSPASS": "Transport",
            "METRO": "Transport",
            "AUTO": "Transport",

            # Entertainment / subscriptions
            "NETFLIX": "Entertainment",
            "SPOTIFY": "Entertainment",
            "AMAZONPRIME": "Entertainment",

            # Tobacco
            "CIGARETTE": "Tobacco",
            "SMOKE": "Tobacco",

            # Utilities (future)
            "ELECTRICITY": "Utilities",
            "WATER": "Utilities",
            "GAS": "Utilities",
        }

    def lookup(self, merchant_name: str):
        """
        Lookup merchant in knowledge base.
        Returns category decision or signals ambiguity.
        """
        
        if not merchant_name:
            return None
        
        merchant_upper = merchant_name.upper()

        for keyword, category in self.merchant_category_map.items():
            if keyword in merchant_upper:
                return category

        return None        
