# test_pipeline_direct.py
from pipeline import ExpenseCategorizationPipeline

pipeline = ExpenseCategorizationPipeline(
    model_path="model.joblib",
    vectorizer_path="vectorizer.joblib"
)

print(
    pipeline.process("CARD/NETFLIX*IN", 199)
)
