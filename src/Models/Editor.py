from sqlalchemy.sql.sqltypes import Date
from Database.Config import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Editor(Base):
	__tablename__ = "editors"

	id = Column(Integer, primary_key=True)
	emailId = Column(String(length=100), unique=True, nullable=False)
	fullName = Column(String(length=100), nullable=False)
	passwordHash = Column(String(length=512), nullable=False)
	phoneNumber = Column(Integer, unique=True)

	created_at = Column(DateTime, default=datetime.utcnow())
	updated_at = Column(DateTime, default=datetime.utcnow())

	def __repr__(self) -> str:
		return self.emailId