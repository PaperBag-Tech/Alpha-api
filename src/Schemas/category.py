from typing import Optional
from pydantic import BaseModel

class CategorySchema(BaseModel):
	name: str
	desp: Optional[str] = None 

