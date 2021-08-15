from typing import List
from pydantic import BaseModel
from datetime import datetime

class Permission(BaseModel):
	object:str 
	access:str

class Role(BaseModel):
	name: str
	desp: str
	permissions: List[Permission]

class RoleRead(Role):
	id: int 
	created_at: datetime
	updated_at: datetime

	class Config:
		orm_mode = True

class RoleWrite(Role):
	pass