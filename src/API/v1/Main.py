from API.V1.endpoints.Category import CategoryRouter
from API.V1.endpoints.Policy import PolicyRouter
from fastapi import APIRouter


router = APIRouter()
router.include_router(CategoryRouter, prefix="/category", tags=["category"])
router.include_router(PolicyRouter, prefix="/policy", tags=["policy"])