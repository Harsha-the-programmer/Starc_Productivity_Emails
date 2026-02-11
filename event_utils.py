from datetime import timedelta

def normalize_event(row):
    start = row["process_start_date"]
    end = row["process_end_date"]

    raw_duration = row["duration"] or 0.0

    if end is None and start is not None:
        end = start + timedelta(seconds=float(raw_duration))

    if start and end:
        duration = (end - start).total_seconds()
    else:
        duration = float(raw_duration)

    is_productive = row["isProductiveApp"]
    productive = bool(is_productive) if is_productive is not None else False

    app_name = row["application_name"] or "Unknown"

    return {
        "start": start,
        "end": end,
        "duration": float(duration),
        "productive": productive,
        "app": app_name
    }
