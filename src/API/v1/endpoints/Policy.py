from fastapi.exceptions import HTTPException
from sqlalchemy.orm import session
from fastapi import APIRouter, Depends
from Schemas.Policy import PolicyWrite, PolicyRead
from typing import List
from Models.Policy import Policy as PolicyModel
from Database.Config import sessionMaker
# from sqlalchemy.dialects.mysql import DATETIME
from datetime import datetime

PolicyRouter = APIRouter()


@PolicyRouter.get("/",response_model=List[PolicyRead])
async def GetAll(db: session = Depends(sessionMaker)):
	"""
	Gets All policies
	"""
	return db.query(PolicyModel).all()

@PolicyRouter.get("/{id}", response_model=PolicyRead)
async def GetById(id: int, db: session = Depends(sessionMaker)):
	return _getPolicy(id, db)
		

@PolicyRouter.post("/", response_model=PolicyRead)
async def Create(data: PolicyWrite, db: session= Depends(sessionMaker)):
	policy = PolicyModel(
		codeName = data.codeName, title = data.title,
		desp = data.desp, categoryId = data.categoryId, details = data.details)
	db.add(policy)
	db.commit()
	return policy

@PolicyRouter.put("/{id}", response_model=PolicyRead)
async def Update(id: int, data: PolicyWrite, db: session = Depends(sessionMaker)):
	policy:PolicyRead = _getPolicy(id, db)
	policy.categoryId = data.categoryId
	policy.codeName = data.codeName
	policy.desp = data.desp
	policy.title = data.title
	policy.details = data.details
	policy.updated_at = datetime.utcnow()
	db.commit()
	return policy

@PolicyRouter.delete("/{id}", response_model=PolicyRead)
async def Delete(id: int, db:session = Depends(sessionMaker)):
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

