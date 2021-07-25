from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
	id: int 
	name: str 
	desp: Optional[str] = None

class Policy(BaseModel):
	id: int 
	category: Category
	codeName: str
	title: str
	desp: str
	details: Optional[list] = None
	
