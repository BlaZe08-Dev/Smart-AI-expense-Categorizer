from fastapi import APIRouter
from pydantic import BaseModel
from User_Overrides import UserOverridesStore

# Router instance
router = APIRouter(
    prefix="/overrides",
    tags=["User Overrides"]
)

# Initialize store
override_store = UserOverridesStore()


# -------- Request Schemas --------
class OverrideRequest(BaseModel):
    merchant: str
    category: str
class RemoveOverrideRequest(BaseModel):
    merchant: str

# -------- API Endpoints --------

@router.post("/add")
def add_override(request: OverrideRequest):
    """
    Add or update a user override:
    Merchant → Category
    """
    override_store.add_override(
        merchant_name=request.merchant,
        category=request.category
    )

    return {
        "status": "success",
        "merchant": request.merchant,
        "category": request.category
    }


@router.get("/all")
def get_all_overrides():
    """
    Get all user-defined overrides
    """
    return {
        "overrides": override_store.overrides
    }


@router.delete("/remove")
def remove_override(request: RemoveOverrideRequest):
    """
    Remove a user-defined override
    """
    removed = override_store.remove_override(request.merchant)

    if not removed:
        return {
            "status": "not_found",
            "merchant": request.merchant
        }

    return {
        "status": "removed",
        "merchant": request.merchant
    }