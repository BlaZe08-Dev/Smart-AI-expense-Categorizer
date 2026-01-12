from Datataker import TransactionDataTaker
from Payment_Mode import TransactionModeDetector
from Merchant_Payment import MerchantExtractor
from Merchant_kb import MerchantKnowledgeBase
from Rule_Engine import RuleBasedClassifier
from AI_Engine import AIcategorizationEngine
from User_Overrides import UserOverridesStore

class ExpenseCategorizationPipeline:
    """
    End-to-end orchestration of the expense categorization system
    """

    def __init__(self, model_path: str, vectorizer_path: str):
        # Step 2
        self.normalizer = TransactionDataTaker()

        # Step 3
        self.mode_detector = TransactionModeDetector()

        # Step 4
        self.merchant_extractor = MerchantExtractor()

        # Step 5
        self.merchant_kb = MerchantKnowledgeBase()
        self.rule_engine = RuleBasedClassifier(self.merchant_kb)
        self.user_overrides = UserOverridesStore()

        # Step 6
        # Step 6 — AI (optional)
        try:
            self.ai_engine = AIcategorizationEngine(
        model_path=model_path,
        vectorizer_path=vectorizer_path)
        except Exception as e:
            print(f"[WARN] AI Engine disabled: {e}")
            self.ai_engine = None


    def process(self, raw_text: str, amount: float | None = None) -> dict:
        """
        Main pipeline entry point
        """
        # STEP 1 — Normalize
        normalized_text = self._safe_normalize(raw_text)

        # STEP 2 — Merchant extraction
        merchant_result = self._safe_extract_merchant(normalized_text)
        merchant = merchant_result.get("merchant")

        # STEP 3 - check user overrides
        user_category = None
        if merchant:
            user_category = self.user_overrides.lookup(merchant)

        if user_category:
            return self._final_response(
                category = user_category,
                confidence = 1.0,
                source = "USER_OVERRIDE",
                 normalized_text = normalized_text,
                 mode = "UNKNOWN",
                 merchant = merchant
            )
        
        # STEP 4 — Mode detection
        mode_result = self._safe_detect_mode(normalized_text)

        # STEP 5 — Rule-based classification
        rule_result = self._safe_rule_classify(
            mode_result=mode_result,
            merchant_result=merchant_result
        )
        # If rules succeeded → return
        if rule_result.get("source") == "RULE":
            return self._final_response(
                category=rule_result.get("category"),
                confidence=rule_result.get("confidence", 1.0),
                source="RULE",
                normalized_text=normalized_text,
                mode=mode_result.get("mode"),
                merchant=merchant
            )
        

        # STEP 6 — AI fallback
        if self.ai_engine is None:
            return self._final_response(
                category=None,
                confidence=0.0,
                source="AI_UNCERTAIN",
                normalized_text=normalized_text,
                mode=mode_result.get("mode"),
                merchant=merchant
            )

        ai_input = self._build_ai_input(
            normalized_text=normalized_text,
            merchant=merchant,
            mode=mode_result.get("mode"),
            amount=amount
        )

        ai_result = self._safe_ai_categorize(ai_input)

        return self._final_response(
            category=ai_result.get("category"),
            confidence=ai_result.get("confidence"),
            source=ai_result.get("source"),
            normalized_text=normalized_text,
            mode=mode_result.get("mode"),
            merchant=merchant
        )

    def _safe_normalize(self, raw_text):
        try:
            if not raw_text:
                return ""
            return self.normalizer.normalizer(raw_text)
        except Exception:
            return ""

    def _safe_detect_mode(self, text):
        try:
            result = self.mode_detector.detect(text)

            if not isinstance(result, dict):
                return {"mode": "UNKNOWN"}
            
            return {"mode": result.get("mode", "UNKNOWN")}
        except Exception:
            return {"mode": "UNKNOWN"}

    def _safe_extract_merchant(self, text):
        try:
            result = self.merchant_extractor.extract(text)
            return {"merchant": result.get("merchant", None)}
        except Exception:
            return {"merchant": None}

    def _safe_rule_classify(self, mode_result, merchant_result):
        try:
            result = self.rule_engine.classify(
                mode_result=mode_result,
                merchant_result=merchant_result
            )
            if result and result.get("category"):
                return {
                    "category": result["category"],
                    "confidence": float(result.get("confidence", 1.0)),
                    "source": "RULE"
                }
            return {"source": "NO_RULE"}
        except Exception:
            return {"source": "NO_RULE"}
        
    def _safe_ai_categorize(self, ai_input):
        # If AI engine was not initialized, return the fallback result immediately.
        if self.ai_engine is None:
            return {
                "category": None,
                "confidence": 0.0,
                "source": "AI_UNCERTAIN"
            }

        try:
            result = self.ai_engine.categorize(ai_input)
            if not result:
                raise ValueError("Empty AI result")

            return {
                "category": result.get("category"),
                "confidence": float(result.get("confidence", 0.0)),
                "source": result.get("source", "AI_UNCERTAIN")
            }
        except Exception:
            return {
                "category": None,
                "confidence": 0.0,
                "source": "AI_UNCERTAIN"
            }    

    def _build_ai_input(self, normalized_text, merchant, mode, amount):
        return {
            "cleaned_text": normalized_text,
            "merchant_hint": merchant,
            "transaction_mode": mode,
            "amount_bucket": self._amount_bucket(amount)
        }

    def _amount_bucket(self, amount):
        if amount is None:
            return None
        if amount < 100:
            return "low"
        if amount < 1000:
            return "medium"
        return "high"

    def _final_response(self, category, confidence, source,normalized_text, mode, merchant, error = None):
        return {
            "category": category,
            "confidence": confidence,
            "source": source,
            "explanation": {
                "normalized_text": normalized_text,
                "mode": mode,
                "merchant": merchant
            }
        }
