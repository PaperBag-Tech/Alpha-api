from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

import Database.Config as dbConfig

class Lead(dbConfig.Base):
	__tablename__ = "leads"

	id = Column(Integer, primary_key=True)
	name = Column(String(length=150), nullable=False)
	phoneNumber = Column(String(length=20), nullable=False, unique=True)
	appointmentTime = Column(DateTime, nullable=False)
	status = Column(String(20), nullable=False)
	agentId = Column(Integer, ForeignKey('users.id'))	

	created_at = Column(DateTime, default=datetime.utcnow())
	updated_at = Column(DateTime, default=datetime.utcnow())
	assignedAgent = relationship("User", back_populates="leads", lazy= True)


	def __repr__(self) -> str:
		return self.name