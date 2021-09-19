from typing import List
from pydantic import BaseModel
from datetime import datetime

import Database.Enums as Constants

class Permission(BaseModel):
	object:str 
	access:str

class Role(BaseModel):
	name: str
	type: Constants.UserRole
	permissions: List[Permission]

class RoleRead(Role):
	id: int 
	created_at: datetime
	updated_at: datetime

	class Config:
		orm_mode = True

class RoleWrite(Role):
	pass