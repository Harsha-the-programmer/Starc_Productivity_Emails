from fastapi import APIRouter
from main import run_daily, run_weekly
from datetime import date
from api.models import DailyRequest, WeeklyRequest

router = APIRouter(prefix="/generate", tags=["Email Generator"])


# DAILY

@router.post("/daily")
def generate_daily_post(data: DailyRequest):
    return _handle_daily(data.user_id, data.date)


@router.get("/daily")
def generate_daily_get(user_id: int, date: date):
    return _handle_daily(user_id, date)


def _handle_daily(user_id: int, day: date):
    email, error = run_daily(user_id, day)

    if error:
        return {"status": "error", "message": error}

    if not email:
        return {"status": "no_trigger"}

    return {
        "status": "success",
        "email": email
    }


# WEEKLY

@router.post("/weekly")
def generate_weekly_post(data: WeeklyRequest):
    return _handle_weekly(data.user_id, data.start_date)


@router.get("/weekly")
def generate_weekly_get(user_id: int, start_date: date):
    return _handle_weekly(user_id, start_date)


def _handle_weekly(user_id: int, start_date: date):
    email, error = run_weekly(user_id, start_date)

    if error:
        return {"status": "error", "message": error}

    if not email:
        return {"status": "no_trigger"}

    return {
        "status": "success",
        "email": email
    }
