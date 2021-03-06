from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

import Database.Config as dbConfig

class Category(dbConfig.Base):
	__tablename__ = "categories"

	id = Column(Integer, primary_key=True)
	name = Column(String(length=50), unique=True, nullable=False)
	desp = Column(String(length=300))
	created_at = Column(DateTime, default=datetime.utcnow())
	updated_at = Column(DateTime, default=datetime.utcnow())

	policies = relationship("Policy", back_populates="category")

	def __repr__(self) -> str:
		return self.name

