from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from Database.Config import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from Models.Role import Role

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	emailId = Column(String(length=100), unique=True, nullable=False)
	fullName = Column(String(length=100), nullable=False)
	passwordHash = Column(String(length=512), nullable=False)
	phoneNumber = Column(Integer, unique=True)
	roleId = Column(Integer, ForeignKey("roles.id"))

	created_at = Column(DateTime, default=datetime.utcnow())
	updated_at = Column(DateTime, default=datetime.utcnow())

	role = relationship(Role, back_populates="users")


	def __repr__(self) -> str:
		return self.emailId