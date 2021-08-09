from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from typing import List
from Database.Config import getDB
from Schemas.User import UserBase, UserLogin, UserPasswordChange, UserRead, UserWrite
from Models.User import User as UserModel
from fastapi.security import OAuth2PasswordBearer


UserRouter = APIRouter()

OAuth2Scheme = OAuth2PasswordBearer(tokenUrl="Login")

@UserRouter.get("/", response_model=List[UserRead], status_code=200)
async def GetAll(db: session = Depends(getDB)):
	"""
	Get all users
	"""
	return db.query(UserModel).all()

@UserRouter.post("/", response_model=UserRead, status_code=201)
async def Create(data: UserWrite ,db: session = Depends(getDB)):
	"""
	Create new user 
	"""
	passwordHash = data.password + "secret"
	user = UserModel(emailId = data.emailId, fullName = data.fullName, 
	phoneNumber = data.phoneNumber, roleId = data.roleId, passwordHash = passwordHash)
	db.add(user)
	db.commit()
	return user

@UserRouter.get("/{id}", response_model=UserRead, status_code=200)
async def GetById(id: int, db: session = Depends(getDB)):
	"""
		Get user by id
	"""
	return getUser(id, db)

@UserRouter.put("/{id}", response_model=UserRead, status_code=200)
async def Update(id: int, data: UserBase, db: session = Depends(getDB), token: str = Depends(OAuth2Scheme)):
	user: UserModel = getUser(id, db)
	user.emailId = data.emailId
	user.fullName = data.fullName
	user.phoneNumber = data.phoneNumber
	user.roleId = data.roleId
	db.commit()
	return user


@UserRouter.delete("/{id}", response_model=UserRead, status_code=202)
async def Delete(id: int, db: session = Depends(getDB), token: str = Depends(OAuth2Scheme)):
	user = getUser(id, db)
	db.delete(user)
	db.commit()
	return user

@UserRouter.put("/changepassword", response_model=bool, status_code=200)
async def ChangePassword(id: int, data:UserPasswordChange, db:session = Depends(getDB)):
	return True

@UserRouter.get("/Login")
async def UserLogin(data: UserLogin, db: session = Depends(getDB)):
	pass

def getUser(id: int, db: session):
	user = db.query(UserModel).filter(id).first()
	if user == None:
		detail = {"error" : f"user record with id {id} is not found."}
		raise HTTPException(404, detail=detail)
	return user