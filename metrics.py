FOCUS_GAP_THRESHOLD_MIN = 5
OVERWORK_THRESHOLD_MIN = 120


def compute_daily_metrics(events):
    metrics = {
        "total_work_min": 0.0,
        "total_non_work_min": 0.0,
        "longest_focus_min": 0.0,
        "overwork_blocks": 0
    }

    if not events:
        return metrics

    events = sorted(events, key=lambda e: e["start"])

    current_focus = 0.0
    last_end = None

    for e in events:
        dur = e["duration"] / 60
        start = e["start"]
        end = e["end"]

        if last_end:
            gap = (start - last_end).total_seconds() / 60
            if gap > FOCUS_GAP_THRESHOLD_MIN:
                if current_focus >= OVERWORK_THRESHOLD_MIN:
                    metrics["overwork_blocks"] += 1
                current_focus = 0.0

        if e["productive"]:
            metrics["total_work_min"] += dur
            current_focus += dur
        else:
            metrics["total_non_work_min"] += dur
            if current_focus >= OVERWORK_THRESHOLD_MIN:
                metrics["overwork_blocks"] += 1
            current_focus = 0.0

        metrics["longest_focus_min"] = max(
            metrics["longest_focus_min"], current_focus
        )

        last_end = end

    if current_focus >= OVERWORK_THRESHOLD_MIN:
        metrics["overwork_blocks"] += 1

    return metrics
