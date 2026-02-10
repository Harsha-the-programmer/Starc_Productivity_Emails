from collections import defaultdict

def compute_weekly_hourly_productivity(events):
    hourly_productive = defaultdict(float)
    hourly_apps = defaultdict(lambda: defaultdict(float))

    for e in events:
        if not e["productive"]:
            continue

        hour = e["start"].hour
        dur = e["duration"] / 60

        hourly_productive[hour] += dur
        hourly_apps[hour][e["app"]] += dur

    return hourly_productive, hourly_apps
