from typing import List
from pydantic import BaseModel
from datetime import datetime

class _PolicyBase(BaseModel):
	codeName: str
	title: str 
	desp: str 
	categoryId: int
	details: str

class PolicyWrite(_PolicyBase):
	pass

class PolicyRead(_PolicyBase):
	id: int
	created_at: datetime
	updated_at: datetime

	class Config:
		orm_mode = True
