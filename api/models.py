from pydantic import BaseModel
from datetime import date


class DailyRequest(BaseModel):
    user_id: int
    date: date


class WeeklyRequest(BaseModel):
    user_id: int
    start_date: date
