import joblib

class AIcategorizationEngine:
    """
    AI fallback engine.
    Called ONLY when rule-based system cannot decide.
    """

    def __init__(self, model_path: str, vectorizer_path: str):
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

        self.accept_threshold = 0.6

    def categorize(self, ai_input: dict) -> dict:
        text_features = self._build_text(ai_input)

        X = self.vectorizer.transform([text_features])
        probabilities = self.model.predict_proba(X)[0]
        predicted_index = probabilities.argmax()

        predicted_category = self.model.classes_[predicted_index]
        confidence  = float(probabilities[predicted_index])

        if confidence >= self.accept_threshold:
            return {
                "source": "AI",
                "category": predicted_category,
                "confidence": confidence,
                "reasoning_tag": "text_pattern_match"
            }
        
        return {
            "source": "AI-UNCERTAIN",
            "category": None,
            "confidence": confidence,
            "reasoning_tag": "low_confidence"
        }
    def _build_text(self, ai_input: dict) -> str:
        """
        Builds final AI text feature from structured input.
        """
        parts =[]

        if ai_input.get("cleaned_text"):
            parts.append(ai_input["cleaned_text"])

        if ai_input.get("merchant_hint"):
            parts.append(ai_input["merchant_hint"])

        if ai_input.get("transaction_hint"):
            parts.append(ai_input["transaction_hint"])

        if ai_input.get("amount_bucket"):
            parts.append(ai_input["amount_bucket"])

        return " ".join(parts)