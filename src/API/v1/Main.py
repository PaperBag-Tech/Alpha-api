from fastapi import APIRouter

import API.V1.Endpoints.Category as Category
import API.V1.Endpoints.Policy as Policy
import API.V1.Endpoints.User as User
import API.V1.Endpoints.Role as Role
import API.V1.Endpoints.Lead as Lead




router = APIRouter()
router.include_router(Category.CategoryRouter, prefix="/category", tags=["Category"])
router.include_router(Policy.PolicyRouter, prefix="/policy", tags=["Policy"])
router.include_router(User.UserRouter, prefix="/user", tags=["User"])
router.include_router(Role.RoleRouter,prefix="/role",tags=["Role"])
router.include_router(Lead.LeadRouter, prefix="/lead",tags=["Lead"])

