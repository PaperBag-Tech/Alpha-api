from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose.constants import ALGORITHMS
from Secrets import secretKey, salt
from passlib.context import CryptContext
from Database.Config import getDB
from sqlalchemy.orm import session
from Models.User import User as UserModel
from Models.Role import Role as RoleModel
from datetime import timedelta, datetime
from jose import jwt, JWTError
from Schemas.User import Token


accessTokenExpiresInMinutes = 30
AuthenticationRouter = APIRouter()
oauth2Scheme = OAuth2PasswordBearer(tokenUrl= "token")
passwordContext = CryptContext(schemes= ["bcrypt"], deprecated= "auto")

def _checkPassword(email: str, password: str, db: session):
	hash = hashPassword(password)
	user = db.query(UserModel).filter(
		UserModel.emailId == email and 
		UserModel.passwordHash == hash).first()
	if user == None:
		raise HTTPException(403, detail={"error" : "Incorrect username or password."})
	return user

def _createAccessToken(data: dict, expries_delta: timedelta):
	expire = datetime.utcnow() + expries_delta
	data.update({"exp":expire})
	encodedJWT = jwt.encode(data,secretKey, algorithm= ALGORITHMS.HS256)
	return encodedJWT

def _getCurrentUserRole(db: session = Depends(getDB), token: str = Depends(oauth2Scheme)):
	credentialsException = HTTPException(401, detail= {"error" : "Could not validate credentials"}, 
					headers={"WWW-Authenticate": "Bearer"})
	try:
		payload = jwt.decode(token, secretKey, algorithms= [ALGORITHMS.HS256])
		email: str = payload.get("sub")
		if datetime.utcnow() > datetime.utcfromtimestamp(int(payload.get("exp"))):
			raise HTTPException(401, detail= {"error" : "session expried login again"}) 
		if email is None:
			raise credentialsException
	except JWTError:
		raise credentialsException
	user: UserModel = db.query(UserModel).filter(UserModel.emailId == email).first()
	if user == None:
		raise credentialsException
	role = db.query(RoleModel).filter(RoleModel.id == user.roleId).first()
	return role

	

def hashPassword(password:str) -> str:
	return passwordContext.hash(password + salt)


class RoleChecker:
	def __init__(self, object: str, access: str) -> None:
		self.object = object
		self.access = access
	
	def __call__(self, role:RoleModel = Depends(_getCurrentUserRole)):
		roles = role.permissions
		roles = roles.split(',')
		if f"{self.object}:{self.access}" in roles:
			return True
		raise HTTPException(401, detail={"error" : "Forbidden request"})
			

@AuthenticationRouter.post("/token", response_model= Token)
async def AccessToken(data: OAuth2PasswordRequestForm = Depends(), db:session = Depends(getDB)):
	user:UserModel = _checkPassword(data.username, data.password, db)
	accessTokenExpires = timedelta(accessTokenExpiresInMinutes)
	access_token = _createAccessToken(data = {"sub" : user.emailId}, expries_delta = accessTokenExpires)
	return { "access_token" : access_token, "token_type" : "bearer" }
