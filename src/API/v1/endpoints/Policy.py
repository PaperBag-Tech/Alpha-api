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

PolicyRouter = APIRouter()


@PolicyRouter.get("/",response_model=List[PolicyRead], status_code=200)
async def GetAll(db: session = Depends(getDB)):
	"""
	Gets All policies
	"""
	return db.query(PolicyModel).all()

@PolicyRouter.get("/{id}", response_model=PolicyRead, status_code=200)
async def GetById(id: int, db: session = Depends(getDB)):
	return _getPolicy(id, db)
		

@PolicyRouter.post("/", response_model=PolicyRead, status_code=201)
async def Create(data: PolicyWrite, db: session= Depends(getDB)):
	category:CategoryRead = _getCategory(data.categoryId, db)
	policy = PolicyModel(
		codeName = data.codeName, title = data.title,
		desp = data.desp, categoryId = category.id, details = data.details)
	db.add(policy)
	db.commit()
	return policy

@PolicyRouter.put("/{id}", response_model=PolicyRead)
async def Update(id: int, data: PolicyWrite, db: session = Depends(getDB)):
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
async def Delete(id: int, db:session = Depends(getDB)):
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

