import re
from typing import Optional


class MerchantExtractor:
    """
    Extracts clean merchant names from noisy bank transaction text.
    """

    # Known big merchants (expand anytime)
    KNOWN_MERCHANTS = [
        "RELIANCE", "JIO", "AMAZON", "FLIPKART",
        "ZOMATO", "SWIGGY", "UBER", "OLA",
        "NETFLIX", "SPOTIFY", "GOOGLE",
        "PAYTM", "PHONEPE", "GPAY"
    ]

    UPI_HANDLE_REGEX = re.compile(r"([a-zA-Z0-9_.]+)@")

    def extract(self, text: str) -> dict:
        if not text:
            return {"merchant": None}

        t = text.upper()

        # -------------------------------
        # 1️⃣ Known merchant keyword match
        # -------------------------------
        for merchant in self.KNOWN_MERCHANTS:
            if merchant in t:
                return {"merchant": merchant}

        # -------------------------------
        # 2️⃣ UPI handle extraction
        # -------------------------------
        m = self.UPI_HANDLE_REGEX.search(t)
        if m:
            handle = m.group(1)
            if len(handle) >= 3:
                return {"merchant": handle.upper()}

        # -------------------------------
        # 3️⃣ Split-based fallback
        # -------------------------------
        parts = re.split(r"[\/|\s]", t)
        blacklist = {"UPI", "DR", "CR", "SBIN", "YESB", "ICICI", "HDFC"}

        for p in parts:
            if (
                len(p) >= 4
                and p.isalpha()
                and p not in blacklist
            ):
                return {"merchant": p}

        # -------------------------------
        # 4️⃣ Nothing usable
        # -------------------------------
        return {"merchant": None}
