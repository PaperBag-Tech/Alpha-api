from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from datetime import datetime
from typing import List

import Schemas.Category as CategoryValidator
import Models.Category as CategoryModel
import Database.Config as dbConfig
import API.Authentication as auth
import Models.User as ModelUser

CategoryRouter = APIRouter()

write = auth.RoleChecker(CategoryModel.Category.__tablename__,"write")
update = auth.RoleChecker(CategoryModel.Category.__tablename__,"update")
delete = auth.RoleChecker(CategoryModel.Category.__tablename__,"delete")

@CategoryRouter.get("/", response_model=List[CategoryValidator.CategoryRead], status_code=200)
async def GetAll(db:session = Depends(dbConfig.getDB)):
	"""
	Get all categories
	"""
	return db.query(CategoryModel.Category).all()

@CategoryRouter.get("/{id}", response_model=CategoryValidator.CategoryRead, status_code=200)
async def GetById(id: int, db:session = Depends(dbConfig.getDB)):
	"""
	Get Category by Id
	"""
	return _getCategory(id, db)

@CategoryRouter.post("/", response_model=CategoryValidator.CategoryRead, status_code=201)
async def Create(data: CategoryValidator.CategoryWrite, db: session = Depends(dbConfig.getDB),access: ModelUser.User = Depends(write)):
	"""
	Creates new Category
	"""
	category = CategoryModel.Category(name = data.name, desp = data.desp)
	db.add(category)
	db.commit()
	return category
	

@CategoryRouter.put("/{id}", response_model=CategoryValidator.CategoryRead, status_code=200)
async def Update(id: int, data: CategoryValidator.CategoryWrite, db:session = Depends(dbConfig.getDB), access: ModelUser.User = Depends(update)):
	category:CategoryValidator.CategoryRead = _getCategory(id, db)
	category.name = data.name
	category.desp = data.desp
	category.updated_at = datetime.utcnow()
	db.commit()
	return category

@CategoryRouter.delete("/{id}", response_model=CategoryValidator.CategoryRead, status_code=202)
async def Delete(id: int, db:session = Depends(dbConfig.getDB), access: ModelUser.User = Depends(delete)):
	"""
	Deletes category by Id
	"""
	category = _getCategory(id, db)
	db.delete(category)
	db.commit()
	return category

def _getCategory(id:int, db:session):
	category = db.query(CategoryModel.Category).filter(CategoryModel.Category.id == id).first()
	if category == None:
		details = {"error" : f"Category with id {id} is not found."}
		raise HTTPException(404, details)
	return category
