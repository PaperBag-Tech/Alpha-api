from pydantic import BaseModel
from datetime import datetime

class Role(BaseModel):
	name: str
	desp: str

class RoleRead(Role):
	id: int 
	created_at: datetime
	updated_at: datetime

class RoleWrite(Role):
	pass