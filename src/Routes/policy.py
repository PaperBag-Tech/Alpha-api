from fastapi import APIRouter
from Schemas.policy import PolicySchema

PolicyRouter = APIRouter(tags=["Policy"])


@PolicyRouter.get("/policy")
async def GetAll():
	"""
	Gets All policies
	"""
	return {"Data": "All Policies"}

@PolicyRouter.get("/policy/{id}")
async def GetById(id: int):
	return {"Data": "{id} policy"}

@PolicyRouter.post("/policy")
async def Create(data: PolicySchema):
	return {"Data": "Policy created"}

@PolicyRouter.put("/policy/{id}")
async def Update(id: int, data: PolicySchema):
	return {"Data": "Policy {id} updated"}

@PolicyRouter.delete("/policy/{id}")
async def Delete(id: int):
	return {"Data":"Policy {id} deleted"}

