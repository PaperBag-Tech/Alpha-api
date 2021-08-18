from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from typing import List
from Database.Config import getDB
from Schemas.User import UserBase, UserPasswordChange, UserRead, UserWrite
from Models.User import User as UserModel
from API.Authentication import hashPassword, RoleChecker
from .Role import _getRole


UserRouter = APIRouter()

read = RoleChecker(UserModel.__tablename__, "read")
write = RoleChecker(UserModel.__tablename__, "write")
update = RoleChecker(UserModel.__tablename__, "update")
delete = RoleChecker(UserModel.__tablename__, "delete")


@UserRouter.put("/change-password", response_model=UserRead, status_code=200)
async def ChangePassword(data:UserPasswordChange, db:session = Depends(getDB)):
	user: UserModel = _getUserByEmail(data.emailId, db)
	if user == None or user.passwordHash == hashPassword(data.oldPassword):
		raise HTTPException(403, detail={"error" : "Incorrect username or password."})
	user.passwordHash = hashPassword(data.newPassword)
	user.updated_at = datetime.utcnow()
	db.commit()
	return user
	

@UserRouter.get("/", response_model=List[UserRead], status_code=200)
async def GetAll(db: session = Depends(getDB), access: bool = Depends(read)):
	"""
	Get all users
	"""
	return db.query(UserModel).all()

@UserRouter.post("/", response_model=UserRead, status_code=201)
async def Create(data: UserWrite ,db: session = Depends(getDB), access: bool = Depends(write)):
	"""
	Create new user 
	"""
	_getRole(data.roleId, db)
	duplicateUser = db.query(UserModel).filter(UserModel.emailId == data.emailId 
	or UserModel.phoneNumber == data.phoneNumber).first()
	if duplicateUser != None:
		raise HTTPException(409, detail= {"error", "Duplicate entry"})
	passwordHash = hashPassword(data.password)
	user = UserModel(emailId = data.emailId, fullName = data.fullName, 
	phoneNumber = data.phoneNumber, roleId = data.roleId, passwordHash = passwordHash)
	db.add(user)
	db.commit()
	return user

@UserRouter.get("/{id}", response_model=UserRead, status_code=200)
async def GetById(id: int, db: session = Depends(getDB), access: bool = Depends(read)):
	"""
		Get user by id
	"""
	return _getUserByid(id, db)

@UserRouter.put("/{id}", response_model=UserRead, status_code=200)
async def Update(id: int, data: UserBase, db: session = Depends(getDB), access: bool = Depends(update)):
	"""
	update the user record
	"""
	user: UserModel = _getUserByid(id, db)
	user.emailId = data.emailId
	user.fullName = data.fullName
	user.phoneNumber = data.phoneNumber
	user.roleId = data.roleId
	db.commit()
	return user

@UserRouter.delete("/{id}", response_model=UserRead, status_code=202)
async def Delete(id: int, db: session = Depends(getDB), access: bool = Depends(delete)):
	user = _getUserByid(id, db)
	db.delete(user)
	db.commit()
	return user	


def _getUserByid(id: int, db: session):
	user = db.query(UserModel).filter(UserModel.id == id).first()
	if user == None:
		raise HTTPException(404, detail={"error" : "user not found."})
	return user

def _getUserByEmail(email: str, db: session):
	user = db.query(UserModel).filter(UserModel.emailId == email).first()
	return user