from datetime import datetime
from typing import Optional
from pydantic import BaseModel

import Database.Enums as Constants
import Schemas.User as UserValidator

class _LeadBase(BaseModel):
	name: str 
	phoneNumber: str 
	appointmentTime: datetime
	agentId: int


class LeadWrite(_LeadBase):
	pass

class LeadReadForCustomer(_LeadBase):
	id: int 
	created_at: datetime
	updated_at: datetime

	class Config:
		orm_mode = True

class LeadUpdateFromAgent(BaseModel):
	status: Constants.LeadStauts
	appointmentTime: Optional[datetime]

class LeadReadForAgent(LeadReadForCustomer):
	status: str
	
	class Config:
		orm_mode = True