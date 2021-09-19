from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose.constants import ALGORITHMS
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import session
from datetime import timedelta, datetime
from jose import jwt, JWTError

import Secrets
import Database.Config as dbConfig
import Models.User as UserModel
import Models.Role as RoleModel
import Schemas.User as UserValidator


accessTokenExpiresInMinutes = 30
AuthenticationRouter = APIRouter()
oauth2Scheme = OAuth2PasswordBearer(tokenUrl= "token")
passwordContext = CryptContext(schemes= ["bcrypt"], deprecated= "auto")

def _checkPassword(email: str, password: str, db: session):
	hash = hashPassword(password)
	user = db.query(UserModel.User).filter(
		UserModel.User.emailId == email and 
		UserModel.User.passwordHash == hash).first()
	if user == None:
		raise HTTPException(403, detail={"error" : "Incorrect username or password."})
	return user

def _createAccessToken(data: dict):
	expire = datetime.utcnow() + timedelta(minutes=accessTokenExpiresInMinutes)
	data.update({"exp":expire})
	encodedJWT = jwt.encode(data,Secrets.secretKey, algorithm= ALGORITHMS.HS256)
	return encodedJWT

def _getCurrentUserRole(db: session = Depends(dbConfig.getDB), token: str = Depends(oauth2Scheme)):
	credentialsException = HTTPException(401, detail= {"error" : "Could not validate credentials"}, 
					headers={"WWW-Authenticate": "Bearer"})
	try:
		payload = jwt.decode(token, Secrets.secretKey, algorithms= [ALGORITHMS.HS256])
		email: str = payload.get("sub")
		if email is None:
			raise credentialsException
	except ExpiredSignatureError:
		raise HTTPException(401, detail= {"error" : "session expried login again"})
	except JWTError:
		raise credentialsException
	user: UserModel = db.query(UserModel.User).filter(UserModel.User.emailId == email).first()
	if user == None:
		raise HTTPException(404, detail= {"error" : "user not found"}) 
	role = db.query(RoleModel.Role).filter(RoleModel.Role.id == user.roleId).first()
	return role

def GetCurrentUser(db: session = Depends(dbConfig.getDB), token: str = Depends(oauth2Scheme)):
	credentialsException = HTTPException(401, detail= {"error" : "Could not validate credentials"}, 
					headers={"WWW-Authenticate": "Bearer"})
	try:
		payload = jwt.decode(token, Secrets.secretKey, algorithms= [ALGORITHMS.HS256])
		email: str = payload.get("sub")
		if email is None:
			raise credentialsException
	except ExpiredSignatureError:
		raise HTTPException(401, detail= {"error" : "session expried login again"})
	except JWTError:
		raise credentialsException
	user: UserModel = db.query(UserModel.User).filter(UserModel.User.emailId == email).first()
	if user == None:
		raise HTTPException(404, detail= {"error" : "user not found"}) 
	return user
	

def hashPassword(password:str) -> str:
	return passwordContext.hash(password + Secrets.salt)


class RoleChecker:
	def __init__(self, object: str, access: str) -> None:
		self.object = object
		self.access = access
	
	def __call__(self, user: UserModel.User = Depends(GetCurrentUser)):
		roles = user.role.permissions
		roles = roles.split(',')
		if f"{self.object}:{self.access}" in roles:
			return user
		raise HTTPException(401, detail={"error" : "Forbidden request"})
			

@AuthenticationRouter.post("/token", response_model= UserValidator.Token)
async def AccessToken(data: OAuth2PasswordRequestForm = Depends(), db:session = Depends(dbConfig.getDB)):
	user:UserModel = _checkPassword(data.username, data.password, db)
	access_token = _createAccessToken(data = {"sub" : user.emailId})
	return { "access_token" : access_token, "token_type" : "bearer" }
