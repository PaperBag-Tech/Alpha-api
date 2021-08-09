from API.V1.Endpoints.Category import CategoryRouter
from API.V1.Endpoints.Policy import PolicyRouter
from API.V1.Endpoints.User import UserRouter
from fastapi import APIRouter


router = APIRouter()
router.include_router(CategoryRouter, prefix="/category", tags=["Category"])
router.include_router(PolicyRouter, prefix="/policy", tags=["Policy"])
router.include_router(UserRouter, prefix="/user", tags=["User"])