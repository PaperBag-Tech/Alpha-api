from pydantic import BaseModel, EmailStr
from datetime import datetime

class EditorBase(BaseModel):
	emailId: EmailStr
	fullName: str 
	phoneNumber: int 


class EditorRead(EditorBase):
	id: int 
	created_at: datetime
	updated_at: datetime 

class EditorWrite(EditorBase):
	password: str

class EditorPassword(BaseModel):
	emailId: EmailStr
	oldPassword: str
	newPassword: str

class EditorLogin(BaseModel):
	emailId: EmailStr
	password: str