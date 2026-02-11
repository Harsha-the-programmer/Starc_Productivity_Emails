SEVERITY = {
    "MEDIUM": "medium",
    "HIGH": "high"
}


def pomodoro_rule(metrics):
    insights = []

    longest_focus = round(metrics.get("longest_focus_min") or 0)
    overwork_blocks = metrics.get("overwork_blocks") or 0

    if overwork_blocks >= 1:
        insights.append({
            "type": "pomodoro",
            "severity": SEVERITY["HIGH"],
            "text": (
                f"You had {overwork_blocks} extended focus session"
                f"{'s' if overwork_blocks > 1 else ''} exceeding two hours "
                "with minimal breaks. Introducing structured short breaks "
                "may help maintain energy and reduce fatigue."
            )
        })

    elif longest_focus >= 90:
        insights.append({
            "type": "pomodoro",
            "severity": SEVERITY["MEDIUM"],
            "text": (
                f"You worked continuously for about {longest_focus} minutes. "
                "Taking short scheduled breaks may help sustain productivity."
            )
        })

    return insights


def weekly_focus_blocks_rule(weekly_hourly, weekly_apps):
    insights = []

    if not weekly_hourly:
        return insights

    WINDOW_SIZE = 2
    hours = sorted(weekly_hourly.keys())

    best_window = None
    best_score = 0

    for h in hours:
        if h + 1 not in weekly_hourly:
            continue

        score = weekly_hourly[h] + weekly_hourly[h + 1]

        if score > best_score:
            best_score = score
            best_window = [h, h + 1]

    if not best_window:
        return insights

    start_hour = best_window[0]
    end_hour = best_window[-1] + 1

    app_usage = {}

    for h in best_window:
        for app, dur in weekly_apps.get(h, {}).items():
            app_usage[app] = app_usage.get(app, 0) + dur

    top_app = max(app_usage, key=app_usage.get) if app_usage else "your primary work tools"

    insights.append({
        "type": "weekly_focus_blocks",
        "start_hour": start_hour,
        "end_hour": end_hour,
        "top_app": top_app,
        "window_minutes": best_score
    })

    return insights

