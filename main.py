from datetime import date
from fetch_data import fetch_events_for_day, fetch_events_for_week, fetch_user_contact_info_from_event_user

from event_utils import normalize_event
from metrics import compute_daily_metrics
from weekly_metrics import compute_weekly_hourly_productivity
from rules import pomodoro_rule, weekly_focus_blocks_rule
from prompt import build_pomodoro_prompt, build_weekly_focus_prompt
from llm import generate_email


TEST_USER_ID = 38167


def run_daily():
    rows = fetch_events_for_day(TEST_USER_ID, day=date(2025, 3, 13))

    if not rows:
        return None, "No daily events found"

    events = [normalize_event(r) for r in rows]
    metrics = compute_daily_metrics(events)

    user = fetch_user_contact_info_from_event_user(TEST_USER_ID)
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


def run_weekly():
    rows = fetch_events_for_week(
        TEST_USER_ID,
        week_start_date=date(2025, 3, 13)
    )

    if not rows:
        return None, "No weekly events found"

    events = [normalize_event(r) for r in rows]

    weekly_hourly, weekly_apps = compute_weekly_hourly_productivity(events)

    insights = weekly_focus_blocks_rule(weekly_hourly, weekly_apps)

    if not insights:
        return None, None

    user = fetch_user_contact_info_from_event_user(TEST_USER_ID)
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


def main():
    daily_email, daily_error = run_daily()

    if daily_error:
        print("Daily error:", daily_error)
    elif daily_email:
        print("\n\n\n------> DAILY POMODORO EMAIL:\n")
        print(daily_email)
    else:
        print("\nNo daily Pomodoro email triggered.\n")

    weekly_email, weekly_error = run_weekly()

    if weekly_error:
        print("Weekly error:", weekly_error)
    elif weekly_email:
        print("\n\n\n-----> WEEKLY FOCUS EMAIL:\n")
        print(weekly_email)
    else:
        print("\nNo weekly focus email triggered.\n")


if __name__ == "__main__":
    main()
