from fastapi.exceptions import HTTPException
from sqlalchemy.orm import session
from fastapi import APIRouter, Depends
from typing import List
from datetime import datetime

import Schemas.Category as CategoryValidator
import Schemas.Policy as PolicyValidator
import Models.Policy as PolicyModel
import Database.Config as dbConfig
import API.V1.Endpoints.Category as Category
import API.Authentication as auth
import Models.User as UserModel


PolicyRouter = APIRouter()

write = auth.RoleChecker(PolicyModel.Policy.__tablename__, "write")
update = auth.RoleChecker(PolicyModel.Policy.__tablename__, "update")
delete = auth.RoleChecker(PolicyModel.Policy.__tablename__, "delete")

@PolicyRouter.get("/",response_model=List[PolicyValidator.PolicyRead], status_code=200)
async def GetAll(db: session = Depends(dbConfig.getDB)):
	"""
		Gets All policies
	"""
	return db.query(PolicyModel.Policy).all()

@PolicyRouter.get("/{id}", response_model=PolicyValidator.PolicyRead, status_code=200)
async def GetById(id: int, db: session = Depends(dbConfig.getDB)):
	"""
		Get policy record by id
	"""
	return _getPolicy(id, db)
		

@PolicyRouter.post("/", response_model=PolicyValidator.PolicyRead, status_code=201)
async def Create(data: PolicyValidator.PolicyWrite, db: session= Depends(dbConfig.getDB), access: UserModel.User = Depends(write)):
	"""
		Create policy record
	"""
	category:CategoryValidator.CategoryRead = Category._getCategory(data.categoryId, db)
	policy = PolicyModel.Policy(
		codeName = data.codeName, title = data.title,
		desp = data.desp, categoryId = category.id, details = data.details)
	db.add(policy)
	db.commit()
	return policy

@PolicyRouter.put("/{id}", response_model=PolicyValidator.PolicyRead, status_code=200)
async def Update(id: int, data: PolicyValidator.PolicyWrite, db: session = Depends(dbConfig.getDB), access: UserModel.User = Depends(update)):
	"""
		updated policy by id
	"""
	policy:PolicyValidator.PolicyRead = _getPolicy(id, db)
	category:CategoryValidator.CategoryRead = Category._getCategory(data.categoryId,db)
	policy.categoryId = category.id
	policy.codeName = data.codeName
	policy.desp = data.desp
	policy.title = data.title
	policy.details = data.details
	policy.updated_at = datetime.utcnow()
	db.commit()
	return policy

@PolicyRouter.delete("/{id}", response_model=PolicyValidator.PolicyRead, status_code=202)
async def Delete(id: int, db:session = Depends(dbConfig.getDB), access: UserModel.User = Depends(delete)):
	"""
		Delete policy by id
	"""
	policy = _getPolicy(id, db)
	db.delete(policy)
	db.commit()
	return policy

def _getPolicy(id:int, db:session):
	policy = db.query(PolicyModel.Policy).filter(PolicyModel.Policy.id == id).first()
	if policy == None:
		details = {"error": f"Policy with id {id} not found."}
		raise HTTPException(404, details)
	return policy

