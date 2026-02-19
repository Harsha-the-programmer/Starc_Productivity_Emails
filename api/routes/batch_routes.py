from fastapi import APIRouter, Query
from datetime import date, timedelta
from fetch_data import get_active_users_for_day
from main import run_daily, run_weekly
import time

router = APIRouter(prefix="/batch", tags=["Batch Jobs"])


def _run_daily_batch(day: date):
    users = get_active_users_for_day(day)
    results = []

    for uid in users:
        email, error = run_daily(uid, day)

        results.append({
            "user_id": uid,
            "email": email,
            "error": error
        })


        time.sleep(0.1)

    return {
        "type": "daily",
        "date": day,
        "total_users": len(users),
        "results": results
    }


def _run_weekly_batch(day: date):
    start = day - timedelta(days=7)
    users = get_active_users_for_day(day)
    results = []

    for uid in users:
        email, error = run_weekly(uid, start)

        results.append({
            "user_id": uid,
            "status": "error" if error else "success" if email else "skipped",
            "error": error
        })

        time.sleep(0.1)

    return {
        "type": "weekly",
        "date": day,
        "week_start": start,
        "total_users": len(users),
        "results": results
    }



@router.post("/daily")
def batch_daily_post(date_param: date | None = None):
    day = date_param or date.today()
    return _run_daily_batch(day)


@router.get("/daily")
def batch_daily_get(date_param: date | None = Query(None)):
    day = date_param or date.today()
    return _run_daily_batch(day)






@router.post("/weekly")
def batch_weekly_post(date_param: date | None = None):
    day = date_param or date.today()
    return _run_weekly_batch(day)


@router.get("/weekly")
def batch_weekly_get(date_param: date | None = Query(None)):
    day = date_param or date.today()
    return _run_weekly_batch(day)
