from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

import Database.Config as dbConfig


class Schedule(dbConfig.Base):
	__tablename__ = "schedules"

	id = Column(Integer, primary_key=True)
	appointment = Column(String(500))
	userId = Column(Integer, ForeignKey("users.id"))

	created_at = Column(DateTime, default=datetime.utcnow())
	updated_at = Column(DateTime, default=datetime.utcnow())


	def __repr__(self) -> str:
		return self.id