from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class _CategoryBase(BaseModel):
	name: str
	desp: Optional[str] = None 

class CategoryWrite(_CategoryBase):
	pass


class CategoryRead(_CategoryBase):
	id: int
	created_at: datetime
	updated_at: datetime

	class Config:
		orm_mode = True


	