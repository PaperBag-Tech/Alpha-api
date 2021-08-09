from Database.Config import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Role(Base):
	__tablename__ = "roles"

	id = Column(Integer, primary_key= True)
	name = Column(String(length=100), unique= True, nullable= False)

	created_at = Column(DateTime, default=datetime.utcnow())
	updated_at = Column(DateTime, default=datetime.utcnow()) 

	users = relationship("User", back_populates="role")

	def __repr__(self) -> str:
		return self.name
