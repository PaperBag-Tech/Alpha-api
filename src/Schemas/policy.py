from typing import List, Optional
from pydantic import BaseModel
from .category import CategorySchema

class PolicySchema(BaseModel):
	categoryId: CategorySchema
	codeName: str
	title: str
	desp: str
	details: Optional[List[str]] = None