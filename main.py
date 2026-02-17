from datetime import date
from fetch_data import fetch_events_for_day, fetch_events_for_week, fetch_user_contact_info_from_event_user

from event_utils import normalize_event
from metrics import compute_daily_metrics
from weekly_metrics import compute_weekly_hourly_productivity
from rules import pomodoro_rule, weekly_focus_blocks_rule
from prompt import build_pomodoro_prompt, build_weekly_focus_prompt
from llm import generate_email

import sys
from datetime import date



def run_daily(user_id: int, day: date):
    rows = fetch_events_for_day(user_id, day=day)

    if not rows:
        return None, "No daily events found"

    events = [normalize_event(r) for r in rows]
    metrics = compute_daily_metrics(events)

    user = fetch_user_contact_info_from_event_user(user_id)
    if not user:
        return None, "User info not found"

    insights = pomodoro_rule(metrics)

    if not insights:
        return None, None

    prompt = build_pomodoro_prompt(
        user_name=user["firstname"],
        date=date.today(),
        metrics=metrics
    )

    email_text = generate_email(prompt)

    return email_text, None


def run_weekly(user_id: int, day: date):
    rows = fetch_events_for_week(user_id, week_start_date=day)

    if not rows:
        return None, "No weekly events found"

    events = [normalize_event(r) for r in rows]

    weekly_hourly, weekly_apps = compute_weekly_hourly_productivity(events)

    insights = weekly_focus_blocks_rule(weekly_hourly, weekly_apps)

    if not insights:
        return None, None

    user = fetch_user_contact_info_from_event_user(user_id)
    if not user:
        return None, "User info not found"

    insight = insights[0]

    prompt = build_weekly_focus_prompt(
        user_name=user["firstname"],
        week_range="Past Week",
        start_hour=insight["start_hour"],
        end_hour=insight["end_hour"],
        top_app=insight["top_app"],
        window_minutes=insight["window_minutes"]
    )

    email_text = generate_email(prompt)

    return email_text, None


def main(user_id: int, day: date):
    daily_email, daily_error = run_daily(user_id=user_id, day=day)

    if daily_error:
        print("Daily error:", daily_error)
    elif daily_email:
        print("\n\n\n------> DAILY POMODORO EMAIL:\n")
        print(daily_email)
    else:
        print("\nNo daily Pomodoro email triggered.\n")

    weekly_email, weekly_error = run_weekly(user_id=user_id, day=day)

    if weekly_error:
        print("Weekly error:", weekly_error)
    elif weekly_email:
        print("\n\n\n-----> WEEKLY FOCUS EMAIL:\n")
        print(weekly_email)
    else:
        print("\nNo weekly focus email triggered.\n")


if __name__ == "__main__":
    user_id = int(sys.argv[1])
    day = date.fromisoformat(sys.argv[2])

    main(user_id, day)
