from Schemas.Category import CategoryRead
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import session
from fastapi import APIRouter, Depends
from Schemas.Policy import PolicyWrite, PolicyRead
from typing import List
from Models.Policy import Policy as PolicyModel
from Database.Config import getDB
from datetime import datetime
from .Category import _getCategory
from API.Authentication import RoleChecker

PolicyRouter = APIRouter()

read = RoleChecker(PolicyModel.__tablename__, "read")
write = RoleChecker(PolicyModel.__tablename__, "write")
update = RoleChecker(PolicyModel.__tablename__, "update")
delete = RoleChecker(PolicyModel.__tablename__, "delete")

@PolicyRouter.get("/",response_model=List[PolicyRead], status_code=200)
async def GetAll(db: session = Depends(getDB)):
	"""
		Gets All policies
	"""
	return db.query(PolicyModel).all()

@PolicyRouter.get("/{id}", response_model=PolicyRead, status_code=200)
async def GetById(id: int, db: session = Depends(getDB)):
	"""
		Get policy record by id
	"""
	return _getPolicy(id, db)
		

@PolicyRouter.post("/", response_model=PolicyRead, status_code=201)
async def Create(data: PolicyWrite, db: session= Depends(getDB), access: bool = Depends(write)):
	"""
		Create policy record
	"""
	category:CategoryRead = _getCategory(data.categoryId, db)
	dulicatePolicy = db.query(PolicyModel).filter(PolicyModel.codeName == data.codeName).first()
	if dulicatePolicy != None:
		raise HTTPException(409, detail= {"error" : "Duplicate entry"})
	policy = PolicyModel(
		codeName = data.codeName, title = data.title,
		desp = data.desp, categoryId = category.id, details = data.details)
	db.add(policy)
	db.commit()
	return policy

@PolicyRouter.put("/{id}", response_model=PolicyRead, status_code=200)
async def Update(id: int, data: PolicyWrite, db: session = Depends(getDB), access: bool = Depends(update)):
	"""
		updated policy by id
	"""
	policy:PolicyRead = _getPolicy(id, db)
	category:CategoryRead = _getCategory(data.categoryId,db)
	policy.categoryId = category.id
	policy.codeName = data.codeName
	policy.desp = data.desp
	policy.title = data.title
	policy.details = data.details
	policy.updated_at = datetime.utcnow()
	db.commit()
	return policy

@PolicyRouter.delete("/{id}", response_model=PolicyRead, status_code=202)
async def Delete(id: int, db:session = Depends(getDB), access: bool = Depends(delete)):
	"""
		Delete policy by id
	"""
	policy = _getPolicy(id, db)
	db.delete(policy)
	db.commit()
	return policy

def _getPolicy(id:int, db:session):
	policy = db.query(PolicyModel).filter(PolicyModel.id == id).first()
	if policy == None:
		details = {"error": f"Policy with id {id} not found."}
		raise HTTPException(404, details)
	return policy

