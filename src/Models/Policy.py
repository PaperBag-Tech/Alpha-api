from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from Database.Config import Base
from datetime import datetime

class Policy(Base):
	__tablename__ = "policies"

	id = Column(Integer, primary_key=True)
	codeName = Column(String(length=50))
	title = Column(String(length=100))
	desp = Column(String(length=300))
	categoryId = Column(Integer, ForeignKey('categories.id'))
	details = Column(String(length=5000))

	created_at = Column(DateTime, default=datetime.utcnow())
	updated_at = Column(DateTime, default=datetime.utcnow())

	category = relationship("Category", back_populates="policies")

	def __repr__(self) -> str:
		return self.codeName
