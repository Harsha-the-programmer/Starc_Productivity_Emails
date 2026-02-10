from collections import defaultdict
# from datetime import timedelta


FOCUS_GAP_THRESHOLD_MIN = 5  


def compute_daily_metrics(events):
    metrics = {
        "total_work_min": 0.0,
        "total_non_work_min": 0.0,
        "longest_focus_min": 0.0,
        "session_count": 0,
        "productive_sessions": 0,
        "non_productive_sessions": 0,
        "hourly_work": defaultdict(float)
    }

    if not events:
        return metrics

    
    events = sorted(events, key=lambda e: e["start"])

    current_focus = 0.0
    last_end = None

    for e in events:
        dur = e["duration"]/60
        start = e["start"]
        end = e["end"]

        metrics["session_count"] += 1

        
        if last_end:
            gap = (start - last_end).total_seconds() / 60
            if gap > FOCUS_GAP_THRESHOLD_MIN:
                current_focus = 0.0

        if e["productive"]:
            metrics["productive_sessions"] += 1
            metrics["total_work_min"] += dur
            current_focus += dur
        else:
            metrics["non_productive_sessions"] += 1
            metrics["total_non_work_min"] += dur
            current_focus = 0.0

        metrics["longest_focus_min"] = max(
            metrics["longest_focus_min"], current_focus
        )

        
        hour = start.hour
        metrics["hourly_work"][hour] += dur

        last_end = end

    return metrics


def productivity_summary(metrics):
    work = round(metrics["total_work_min"])
    non_work = round(metrics["total_non_work_min"])
    total = work + non_work

    if total == 0:
        return None

    ratio = work / total

    if ratio < 0.5:
        return (
            f"Out of {total} total minutes, only {work} minutes were productive, "
            f"indicating frequent interruptions or task switching."
        )
    elif ratio < 0.7:
        return (
            f"Out of {total} total minutes, {work} minutes were productive, "
            f"suggesting a mixed balance of focused and non-focused work."
        )
    else:
        return (
            f"Out of {total} total minutes, {work} minutes were spent on productive work, "
            f"showing strong task engagement."
        )
