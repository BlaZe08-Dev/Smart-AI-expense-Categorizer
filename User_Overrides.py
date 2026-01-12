import json
import os

class UserOverridesStore:
    def __init__(self, file_path="user_overrides.json"):
        self.file_path = file_path
        self.overrides = self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.overrides, f, indent=2)

    def lookup(self, merchant_name: str):
        if not merchant_name:
            return None

        merchant_upper = merchant_name.upper()
    
    # Exact match first
        if merchant_upper in self.overrides:
            return self.overrides[merchant_upper]

    # Partial match fallback
        for saved_merchant, category in self.overrides.items():
            if saved_merchant in merchant_upper:
                return category

        return None

    
    def add_override(self, merchant_name: str, category: str):
        clean_category = category.strip().title()
        self.overrides[merchant_name.upper()] = clean_category
        self._save()

    def remove_override(self, merchant_name: str):
        key = merchant_name.upper()
        if key in self.overrides:
            del self.overrides[key]
            self._save()
            return True
        return False