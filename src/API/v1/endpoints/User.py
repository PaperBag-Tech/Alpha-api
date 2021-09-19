from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.datastructures import DefaultPlaceholder
from sqlalchemy.orm import session
from typing import List
from datetime import date, time

import Database.Config as dbConfig
import Schemas.User as UserValidator
import Models.User as UserModel
import API.Authentication as auth
import Database.Enums as Constants
import API.V1.Endpoints.Role as RoleRouter
import Schemas.Role as RoleValidator
import Models.Role as RoleModel
import Schemas.Schedule as ScheduleValidator


UserRouter = APIRouter()

read = auth.RoleChecker(UserModel.User.__tablename__, "read")
write = auth.RoleChecker(UserModel.User.__tablename__, "write")
update = auth.RoleChecker(UserModel.User.__tablename__, "update")
delete = auth.RoleChecker(UserModel.User.__tablename__, "delete")


@UserRouter.put("/change-password", response_model=UserValidator.UserRead, status_code=200)
async def ChangePassword(data:UserValidator.UserPasswordChange, db:session = Depends(dbConfig.getDB)):
	user: UserModel.User = _getUserByEmail(data.emailId, db)
	if user == None or user.passwordHash == auth.hashPassword(data.oldPassword):
		raise HTTPException(403, detail={"error" : "Incorrect username or password."})
	user.passwordHash = auth.hashPassword(data.newPassword)
	user.updated_at = datetime.utcnow()
	db.commit()
	return _convertTimePeriodModelToRead([user])[0]


@UserRouter.get("/Agents", response_model=List[UserValidator.UserRead], status_code=200)
async def GetAllAgents(db: session = Depends(dbConfig.getDB)):
	"""
	Get all agent
	"""
	agentRole: RoleModel.Role = db.query(RoleModel.Role).filter(
		RoleModel.Role.type == Constants.UserRole.Agent).first()
	return _convertTimePeriodModelToRead(db.query(UserModel.User).filter(UserModel.User.roleId == agentRole.id).all())

@UserRouter.get("Agent/{id}", response_model=UserValidator.UserRead, status_code=200)
async def GetAgentById(id: int, db: session = Depends(dbConfig.getDB)):
	"""
	Get agent detials by id
	"""
	return _convertTimePeriodModelToRead([_getUserByid(id,db)])[0]

@UserRouter.get("/Slots/{id}",response_model=UserValidator.Slots, status_code= 200)
async def GetAgentSlots(id: int, date: date, db: session = Depends(dbConfig.getDB)):
	user: UserModel.User = _getUserByid(id, db)
	userRole: RoleModel.Role = db.query(RoleModel.Role).filter(RoleModel.Role.id == user.id).first()
	if userRole.type != Constants.UserRole.Agent:
		raise HTTPException(400, detail={"error", f"Requested user with id {id} is not agent"})
	slots = []
	for lead in user.leads:
		appDate = datetime(lead.appointmentTime.year, lead.appointmentTime.month, lead.appointmentTime.day)
		if appDate.date() == date:
			slots.append(lead.appointmentTime)
	Slots = UserValidator.Slots(slots = slots)
	return Slots

@UserRouter.get("/", response_model=List[UserValidator.UserRead], status_code=200)
async def GetAll(db: session = Depends(dbConfig.getDB), access: bool = Depends(read)):
	"""
	Get all users
	"""
	users = db.query(UserModel.User).all()
	return _convertTimePeriodModelToRead(users)

@UserRouter.post("/", response_model=UserValidator.UserRead, status_code=201)
async def Create(data: UserValidator.UserWrite ,db: session = Depends(dbConfig.getDB), access: bool = Depends(write)):
	"""
	Create new user 
	"""
	role: RoleValidator.RoleRead = RoleRouter._getRole(data.roleId,db)
	if role.type == Constants.UserRole.Agent and data.workingHours == None:
		raise HTTPException(400, detail={"error", "For agent working hours is requried"})
	passwordHash = auth.hashPassword(data.password)
	workingHours = []
	for timePeriod in data.workingHours:
		workingHours.append(f"{timePeriod.startTime}->{timePeriod.endTime}")
	user = UserModel.User(emailId = data.emailId, fullName = data.fullName, 
	phoneNumber = data.phoneNumber, roleId = role.id, passwordHash = passwordHash)
	user.workingHours = ",".join(workingHours)
	db.add(user)
	db.commit()
	return _convertTimePeriodModelToRead([user])[0]

@UserRouter.get("/{id}", response_model=UserValidator.UserRead, status_code=200)
async def GetById(id: int, db: session = Depends(dbConfig.getDB), access: bool = Depends(read)):
	"""
		Get user by id
	"""
	return _convertTimePeriodModelToRead([_getUserByid(id, db)])[0]

@UserRouter.put("/{id}", response_model=UserValidator.UserRead, status_code=200)
async def Update(id: int, data: UserValidator.UserBase, db: session = Depends(dbConfig.getDB), access: bool = Depends(update)):
	"""
	update the user record
	"""
	user: UserModel.User = _getUserByid(id, db)
	user.emailId = data.emailId
	user.fullName = data.fullName
	user.phoneNumber = data.phoneNumber
	user.roleId = data.roleId
	if data.workingHours != None:
		workingHours = []
		for timeperiod in data.workingHours:
			workingHours.append(f"{timeperiod.startTime}->{timeperiod.endTime}")
		user.workingHours = ','.join(workingHours)
	db.commit()
	return _convertTimePeriodModelToRead([user])[0]

@UserRouter.delete("/{id}", response_model=UserValidator.UserRead, status_code=202)
async def Delete(id: int, db: session = Depends(dbConfig.getDB), access: bool = Depends(delete)):
	user = _getUserByid(id, db)
	db.delete(user)
	db.commit()
	return _convertTimePeriodModelToRead([user])[0]


def _getUserByid(id: int, db: session):
	user = db.query(UserModel.User).filter(UserModel.User.id == id).first()
	if user == None:
		raise HTTPException(404, detail={"error" : "user not found."})
	return user

def _getUserByEmail(email: str, db: session):
	user = db.query(UserModel.User).filter(UserModel.User.emailId == email).first()
	return user

def _convertTimePeriodModelToRead(data: List[UserModel.User]) -> List[UserValidator.UserRead]:
	for user in data:
		if user.workingHours != None:
			workingHours = []
			workingHoursStr = user.workingHours.split(",")
			for timePeriod in workingHoursStr:
				period = timePeriod.split("->")
				outputPeriod = ScheduleValidator.TimePeriod(
					startTime = period[0], endTime = period[1])
			workingHours.append(outputPeriod)
			user.workingHours = workingHours
	return data

	