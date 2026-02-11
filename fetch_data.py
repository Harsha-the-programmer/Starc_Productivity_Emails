from datetime import datetime, timedelta
from db import get_connection


IST_OFFSET = timedelta(hours=5, minutes=30)


def convert_to_ist(dt):
    if dt:
        return dt + IST_OFFSET
    return dt


def subtract_private_intervals(event_start, event_end, private_intervals):
    total_seconds = (event_end - event_start).total_seconds()

    for p_start, p_end in private_intervals:
        overlap_start = max(event_start, p_start)
        overlap_end = min(event_end, p_end)

        if overlap_start < overlap_end:
            total_seconds -= (overlap_end - overlap_start).total_seconds()

    return max(0, int(total_seconds))


def fetch_private_intervals(systemname, start_dt, end_dt):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = """
        SELECT
            private_mode_start_time,
            private_mode_end_time
        FROM tbl_privatemode
        WHERE systemname = %s
          AND private_mode_start_time < %s
          AND private_mode_end_time > %s
    """

    cursor.execute(query, (systemname, end_dt, start_dt))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    intervals = []
    for row in rows:
        intervals.append(
            (
                row["private_mode_start_time"],
                row["private_mode_end_time"]
            )
        )

    return intervals


def fetch_events_for_day(user_id, day=None, limit=5000):
    if day is None:
        day = datetime.utcnow().date() - timedelta(days=1)

    start_dt = datetime.combine(day, datetime.min.time())
    end_dt = start_dt + timedelta(days=1)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = """
        SELECT
            event_id,
            user_id,
            mac_id,
            application_name,
            process_start_date,
            process_end_date,
            duration,
            isProductiveApp,
            user_name
        FROM processed_users_events
        WHERE user_id = %s
          AND application_name NOT IN ('Shutdown', 'IdleTime')
          AND process_start_date >= %s
          AND process_start_date < %s
        ORDER BY process_start_date
        LIMIT %s
    """

    cursor.execute(query, (user_id, start_dt, end_dt, limit))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return []

    systemname = rows[0]["user_name"]

    private_intervals = fetch_private_intervals(systemname, start_dt, end_dt)

    refined_rows = []

    for row in rows:
        start_time = row["process_start_date"]
        end_time = row["process_end_date"]

        adjusted_seconds = subtract_private_intervals(
            start_time,
            end_time,
            private_intervals
        )

        if adjusted_seconds <= 0:
            continue

        row["duration"] = adjusted_seconds
        row["process_start_date"] = convert_to_ist(start_time)
        row["process_end_date"] = convert_to_ist(end_time)

        refined_rows.append(row)

    return refined_rows



def fetch_user_contact_info_from_event_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = """
        SELECT
            tu.id,
            tu.firstname,
            tu.lastname,
            tu.email,
            tu.phoneNo
        FROM processed_users_events pe
        JOIN users_systemdetails usd
            ON pe.mac_id = usd.macid
           AND pe.user_name = usd.systemname
           AND usd.is_active = 1
        JOIN tbl_users tu
            ON usd.user_id = tu.id
        WHERE pe.user_id = %s
        LIMIT 1
    """

    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def fetch_events_for_week(user_id, week_start_date):
    start_dt = datetime.combine(week_start_date, datetime.min.time())
    end_dt = start_dt + timedelta(days=7)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = """
        SELECT
            application_name,
            process_start_date,
            process_end_date,
            duration,
            isProductiveApp,
            mac_id,
            user_name
        FROM processed_users_events
        WHERE user_id = %s
          AND application_name NOT IN ('Shutdown', 'IdleTime')
          AND process_start_date >= %s
          AND process_start_date < %s
        ORDER BY process_start_date
    """

    cursor.execute(query, (user_id, start_dt, end_dt))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    private_intervals = fetch_private_intervals(user_id, start_dt, end_dt)

    refined_rows = []

    for row in rows:
        start_time = row["process_start_date"]
        end_time = row["process_end_date"]

        adjusted_seconds = subtract_private_intervals(
            start_time,
            end_time,
            private_intervals
        )

        if adjusted_seconds <= 0:
            continue

        row["duration"] = adjusted_seconds
        row["process_start_date"] = convert_to_ist(start_time)
        row["process_end_date"] = convert_to_ist(end_time)

        refined_rows.append(row)

    return refined_rows
