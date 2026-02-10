def normalize_event(row):
    start = row["process_start_date"]
    end = row["process_end_date"]

    
    if end is None:
        end = start

    duration = row["duration"] or 0.0


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
