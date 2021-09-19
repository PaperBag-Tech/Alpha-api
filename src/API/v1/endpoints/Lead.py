from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session

import Models.Lead as LeadModel
import Models.User as UserModel 
import Models.Role as RoleModel
import Schemas.Lead as LeadValidator
import Database.Config as dbConfig
import Database.Enums as Constants
import API.Authentication as auth
 


LeadRouter = APIRouter()

update = auth.RoleChecker(LeadModel.Lead.__tablename__, "update")
read = auth.RoleChecker(LeadModel.Lead.__tablename__, "read")
delete = auth.RoleChecker(LeadModel.Lead.__tablename__, "delete")

@LeadRouter.get("/", response_model=List[LeadValidator.LeadReadForAgent], status_code= 200)
async def GetAll(db: session = Depends(dbConfig.getDB), access: UserModel.User = Depends(read)):
	leads = db.query(LeadModel.Lead).all()
	return leads

@LeadRouter.get("/My", response_model=List[LeadValidator.LeadReadForAgent], status_code=200)
async def GetMyLeads(db: session = Depends(dbConfig.getDB), access: UserModel.User = Depends(auth.GetCurrentUser)):
	return db.query(LeadModel.Lead).filter(LeadModel.Lead.agentId == access.id).all()

@LeadRouter.post("/Create",response_model=LeadValidator.LeadReadForCustomer, status_code=201)
async def Create(data: LeadValidator.LeadWrite, db:session = Depends(dbConfig.getDB)):
	duplicateLead = db.query(LeadModel.Lead).filter(LeadModel.Lead.phoneNumber == data.phoneNumber).first()
	if duplicateLead != None:
		return duplicateLead
	agent: UserModel.User = db.query(UserModel.User).join(RoleModel.Role).filter(
		RoleModel.Role.type == Constants.UserRole.Agent and 
		RoleModel.Role.id == data.agentId).first()
	lead: LeadModel.Lead
	if agent != None:
		lead = LeadModel.Lead(name = data.name, phoneNumber = data.phoneNumber, 
			appointmentTime = data.appointmentTime, status = Constants.LeadStauts.scheduled, agentId = agent.id)
	else:
		raise HTTPException(404, detail={"error" : f"Agent with id {data.agentId} is not found"})
	db.add(lead)
	db.commit()
	db.refresh(lead)
	return lead

@LeadRouter.put("/update", response_model=LeadValidator.LeadReadForAgent, status_code=200)
async def Update(id: int, data: LeadValidator.LeadUpdateFromAgent, db:session = Depends(dbConfig.getDB), access: UserModel.User = Depends(update)):
	lead: LeadModel.Lead = _getLead(id, db)
	lead.status = data.status
	if data.appointmentTime != None:
		lead.appointmentTime = data.appointmentTime
	db.commit()
	return lead

@LeadRouter.delete("/delete", response_model=LeadValidator.LeadReadForAgent, status_code= 202)
async def Delete(id: int, db: session = Depends(dbConfig.getDB), access: UserModel.User = Depends(delete)):
	lead: LeadModel.Lead = _getLead(id, db)
	db.delete(lead)
	db.commit()
	return lead

def _getLead(id: int, db: session):
	lead = db.query(LeadModel.Lead).filter(LeadModel.Lead.id == id).first()
	if lead == None:
		raise HTTPException(404, detail= {"error" : f"lead with id {id} is not found"})
	return lead