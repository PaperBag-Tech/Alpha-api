from datetime import time
from pydantic import BaseModel
from typing import List


class TimePeriod(BaseModel):
	startTime: time
	endTime: time

class _BaseSchedule(BaseModel):
	userId: int 
	appointments: List[TimePeriod]

class ScheduleWrite(_BaseSchedule):
	pass

class ScheduleRead(_BaseSchedule):
	id: int 
	created_at: time
	update_at: time


