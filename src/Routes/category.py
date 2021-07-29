from fastapi import APIRouter
from Schemas.category import CategorySchema

CategoryRouter = APIRouter(tags= ["Category"])

@CategoryRouter.get("/category")
async def GetAll():
	"""
	Get all category
	"""
	return {"Data":"All Categories"}

@CategoryRouter.post("/category")
async def Create(data: CategorySchema):
	"""
	Creates new Category
	"""
	return {"Data":"Created Category"}

@CategoryRouter.get("/category/{id}")
async def GetById(id: int):
	return {"Data":"Category {id}"}

@CategoryRouter.put("/category/{id}")
async def Updated(id: int, data: CategorySchema):
	return {"Data": "Category {id} updated"}

@CategoryRouter.delete("/category/{id}")
async def Delete(id: int):
	return {"Data": "Category {id} deleted"}
