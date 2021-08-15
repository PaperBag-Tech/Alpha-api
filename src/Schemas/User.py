from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
	emailId: EmailStr
	fullName: str 
	phoneNumber: str
	roleId: int


class UserRead(UserBase):
	id: int 
	created_at: datetime
	updated_at: datetime 

	class Config:
		orm_mode = True

class UserWrite(UserBase):
	password: str

class UserPasswordChange(BaseModel):
	emailId: EmailStr
	oldPassword: str
	newPassword: str

class UserLogin(BaseModel):
	emailId: EmailStr
	password: str

class Token(BaseModel):
	access_token: str
	token_type: str