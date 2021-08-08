from API.V1.endpoints.Category import CategoryRouter
from API.V1.endpoints.Policy import PolicyRouter
from API.V1.endpoints.Editor import EditorRouter
from fastapi import APIRouter


router = APIRouter()
router.include_router(CategoryRouter, prefix="/category", tags=["Category"])
router.include_router(PolicyRouter, prefix="/policy", tags=["Policy"])
router.include_router(EditorRouter, prefix="/editor", tags=["Editor"])