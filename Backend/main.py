from fastapi import FastAPI

from .api.categorize_api import router as categorize_router
from .api.override_api import router as override_router
from .api.analytics_api import router as analytics_router
from .api.bulk_api import router as bulk_router
from .api.ingest_api import router as ingest_router
from .api.pdf_api import router as pdf_router

app = FastAPI(
    title="Smart AI Expense Categorizer",
    description="Hybrid rule-based + AI expense categorization system",
    version="1.0"
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mount APIs
app.include_router(categorize_router)
app.include_router(override_router)
app.include_router(analytics_router)
app.include_router(bulk_router)
app.include_router(ingest_router)
app.include_router(pdf_router)