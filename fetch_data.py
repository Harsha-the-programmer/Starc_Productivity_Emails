from datetime import datetime, timedelta
from db import get_connection


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
            isProductiveApp
        FROM processed_users_events
        WHERE user_id = %s
          AND application_id <> 14378
          AND process_start_date >= %s
          AND process_start_date < %s
        ORDER BY process_start_date
        LIMIT %s
    """

    cursor.execute(query, (user_id, start_dt, end_dt, limit))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def fetch_user_contact_info_from_event_user(event_user_id):
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
        JOIN desktop_users du
            ON pe.user_id = du.user_id
        JOIN users_systemdetails usd
            ON du.mac_id = usd.macid
        JOIN tbl_users tu
            ON usd.user_id = tu.id
        WHERE pe.user_id = %s
        LIMIT 1
    """

    cursor.execute(query, (event_user_id,))
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
            isProductiveApp
        FROM processed_users_events
        WHERE user_id = %s
          AND application_id <> 14378
          AND process_start_date >= %s
          AND process_start_date < %s
        ORDER BY process_start_date
    """

    cursor.execute(query, (user_id, start_dt, end_dt))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
