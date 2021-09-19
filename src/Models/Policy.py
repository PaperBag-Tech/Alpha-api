from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime

import Database.Config as dbConfig
import Models.Category as CategoryModel

class Policy(dbConfig.Base):
	__tablename__ = "policies"

	id = Column(Integer, primary_key=True)
	codeName = Column(String(length=50), unique= True, nullable= False)
	title = Column(String(length=100), nullable= False)
	desp = Column(String(length=300))
	categoryId = Column(Integer, ForeignKey('categories.id'))
	details = Column(String(length=5000))

	created_at = Column(DateTime, default=datetime.utcnow())
	updated_at = Column(DateTime, default=datetime.utcnow())

	category = relationship(CategoryModel.Category, back_populates="policies")

	def __repr__(self) -> str:
		return self.codeName

