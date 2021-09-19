from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

import Schemas.Schedule as ScheduleValidator

class UserBase(BaseModel):
	emailId: EmailStr
	fullName: str 
	phoneNumber: str
	roleId: int
	workingHours: Optional[List[ScheduleValidator.TimePeriod]]


class UserRead(UserBase):
	id: int 
	appointment: Optional[List[ScheduleValidator.ScheduleRead]]
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

class Slots(BaseModel):
	slots: List[datetime]