from collections import defaultdict
from datetime import timedelta


def compute_weekly_hourly_productivity(events):
    hourly_productive = defaultdict(float)
    hourly_apps = defaultdict(lambda: defaultdict(float))

    for e in events:
        if not e["productive"]:
            continue

        start = e["start"]
        end = e["end"]
        app = e["app"]

        current = start

        while current < end:
            next_hour = (current.replace(minute=0, second=0, microsecond=0)
                         + timedelta(hours=1))

            segment_end = min(end, next_hour)
            segment_minutes = (segment_end - current).total_seconds() / 60

            hour = current.hour

            hourly_productive[hour] += segment_minutes
            hourly_apps[hour][app] += segment_minutes

            current = segment_end

    return hourly_productive, hourly_apps


def compute_weekly_focus_windows(hourly_productive):
    window_scores = {}

    for hour in range(0, 23):
        two_hour_total = (
            hourly_productive.get(hour, 0) +
            hourly_productive.get(hour + 1, 0)
        )

        window_scores[(hour, hour + 2)] = two_hour_total

    best_window = max(window_scores, key=window_scores.get)

    return {
        "best_window": best_window,
        "best_window_minutes": window_scores[best_window],
        "all_windows": window_scores
    }
