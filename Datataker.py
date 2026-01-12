import re

class TransactionDataTaker:
    def __init__(self):
        self.currency_symbols = re.compile(r'[\$\€\£\₹]')
        self.multiple_spaces = re.compile(r'\s+')
        self.numeric_noise = re.compile(r"\b\d+\b")

    def normalizer(self,raw_text: str) -> str:
        """
        Normalize raw transaction text to clean format.
        """

        if not raw_text or not isinstance(raw_text, str):
            return""
        
        text = raw_text.lower()

        # remove currency symbols
        text = self.currency_symbols.sub("", text)

        # replace separators with space
        text = text.replace("/", " ").replace("-", " ").replace("*", " ")

         # remove standalone numbers (txn ids, phone numbers)
        text = self.numeric_noise.sub("", text)

        # remove special characters except letters
        text = re.sub(r"[^a-z\s]", " ", text)

        # normalize whitespace
        text = self.multiple_spaces.sub(" ", text).strip()

        
        return text