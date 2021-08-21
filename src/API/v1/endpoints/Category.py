from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from Schemas.Category import CategoryWrite, CategoryRead
from typing import List
from Models.Category import Category as CategoryModel
from Database.Config import getDB
from datetime import datetime
from API.Authentication import RoleChecker

CategoryRouter = APIRouter()

read = RoleChecker(CategoryModel.__tablename__,"read")
write = RoleChecker(CategoryModel.__tablename__,"write")
update = RoleChecker(CategoryModel.__tablename__,"update")
delete = RoleChecker(CategoryModel.__tablename__,"delete")

@CategoryRouter.get("/", response_model=List[CategoryRead], status_code=200)
async def GetAll(db:session = Depends(getDB)):
	"""
	Get all categories
	"""
	return db.query(CategoryModel).all()

@CategoryRouter.get("/{id}", response_model=CategoryRead, status_code=200)
async def GetById(id: int, db:session = Depends(getDB)):
	"""
	Get Category by Id
	"""
	return _getCategory(id, db)

@CategoryRouter.post("/", response_model=CategoryRead, status_code=201)
async def Create(data: CategoryWrite, db: session = Depends(getDB),access: bool = Depends(write)):
	"""
	Creates new Category
	"""
	category = CategoryModel(name = data.name, desp = data.desp)
	db.add(category)
	db.commit()
	return category
	

@CategoryRouter.put("/{id}", response_model=CategoryRead, status_code=200)
async def Update(id: int, data: CategoryWrite, db:session = Depends(getDB), access: bool = Depends(update)):
	category:CategoryRead = _getCategory(id, db)
	category.name = data.name
	category.desp = data.desp
	category.updated_at = datetime.utcnow()
	db.commit()
	return category

@CategoryRouter.delete("/{id}", response_model=CategoryRead, status_code=202)
async def Delete(id: int, db:session = Depends(getDB), access: bool = Depends(delete)):
	"""
	Deletes category by Id
	"""
	category = _getCategory(id, db)
	db.delete(category)
	db.commit()
	return category

def _getCategory(id:int, db:session):
	category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
	if category == None:
		details = {"error" : f"Category with id {id} is not found."}
		raise HTTPException(404, details)
	return category
