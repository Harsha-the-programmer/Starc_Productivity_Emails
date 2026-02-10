from fetch_data import fetch_events_for_day, fetch_user_contact_info_from_event_user
from event_utils import normalize_event
from metrics import compute_daily_metrics
from rules import pomodoro_rule, focus_blocks_rule
from prompt import build_prompt
from datetime import date
from llm import generate_email
from fetch_data import fetch_events_for_week
from weekly_metrics import compute_weekly_hourly_productivity
from rules import weekly_focus_blocks_rule



TEST_USER_ID = 38167


def main():
    email, error = run_once()

    if error:
        print("Error: ", error)
        return

    print("\nGENERATED EMAIL:\n")
    print(email)

"""
def main():
    rows = fetch_events_for_day(TEST_USER_ID,day=date(2025, 3, 6))
    print(f"\n\nEvents fetched: {len(rows)}")

    if not rows:
        print("No events found")
        return

    events = [normalize_event(r) for r in rows]
    metrics = compute_daily_metrics(events)

    print("Metrics computed:")
    print(f"  Total work minutes      : {metrics['total_work_min']}")
    print(f"  Longest focus (minutes) : {metrics['longest_focus_min']}")

    user = fetch_user_contact_info_from_event_user(TEST_USER_ID)

    if not user:
        print("Could not find user info")
        return

    print("\nUser:")
    print(f"  Name  : {user['firstname']} {user['lastname']}")
    print(f"  Email : {user['email']}")

    insights = []
    insights.extend(pomodoro_rule(metrics))
    insights.extend(focus_blocks_rule(metrics))

    prompt = build_prompt(
        user_name=user["firstname"],
        date=date.today(),
        metrics=metrics,
        insights=insights
    )

    print("\n\n\nPROMPT:\n")
    print(prompt)

    
    email_text = generate_email(prompt)

    print("\n\nGENERATED EMAIL:\n")
    print(email_text)

"""

def run_once():
    rows = fetch_events_for_day(TEST_USER_ID, day=date(2025, 3, 5))

    if not rows:
        return None, "No events found"

    events = [normalize_event(r) for r in rows]
    metrics = compute_daily_metrics(events)

    user = fetch_user_contact_info_from_event_user(TEST_USER_ID)
    if not user:
        return None, "User info not found"

    insights = []
    insights.extend(pomodoro_rule(metrics))
    insights.extend(focus_blocks_rule(metrics))

    # Weekly focus analysis
    week_events_raw = fetch_events_for_week(
        TEST_USER_ID,
        week_start_date=date(2025, 3, 5)
    )

    week_events = [normalize_event(r) for r in week_events_raw]

    weekly_productive_minutes = sum(
        e["duration"] / 60
        for e in week_events
        if e["productive"]
    )
    weekly_productive_minutes = round(weekly_productive_minutes)


    weekly_hourly, weekly_apps = compute_weekly_hourly_productivity(week_events)

    insights.extend(
        weekly_focus_blocks_rule(weekly_hourly, weekly_apps)
    )

    weekly_focus_text = None

    for i in insights:
        if i["type"] == "weekly_focus_blocks":
            weekly_focus_text = i["text"]
            break


    prompt = build_prompt(
        user_name=user["firstname"],
        date=date.today(),
        metrics=metrics,
        insights=insights,
        weekly_focus_text=weekly_focus_text,
        weekly_productive_minutes=weekly_productive_minutes,
    )

    email_text = generate_email(prompt)

    return email_text, None


if __name__ == "__main__":
    main()
