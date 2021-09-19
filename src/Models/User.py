from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

import Database.Config as dbConfig
import Models.Role as RoleModel
import Models.Lead as LeadModel
import Models.Schedule as ScheduleModel

class User(dbConfig.Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	emailId = Column(String(length=100), unique=True, nullable=False)
	fullName = Column(String(length=100), nullable=False)
	passwordHash = Column(String(length=512), nullable=False)
	phoneNumber = Column(String(length=15), unique=True)
	workingHours = Column(String(length=200))
	roleId = Column(Integer, ForeignKey("roles.id"))

	created_at = Column(DateTime, default=datetime.utcnow())
	updated_at = Column(DateTime, default=datetime.utcnow())

	role = relationship(RoleModel.Role, back_populates="users")
	leads = relationship(LeadModel.Lead, back_populates="assignedAgent")

	def __repr__(self) -> str:
		return self.emailId