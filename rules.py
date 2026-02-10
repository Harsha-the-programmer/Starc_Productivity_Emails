SEVERITY = {
    "MEDIUM": "medium",
    "HIGH": "high"
}

def pomodoro_rule(metrics):
    insights = []

    longest_focus = metrics.get("longest_focus_min") or 0

    
    if longest_focus <= 0:
        return insights

    longest_focus = round(longest_focus)

    
    if longest_focus >= 90:
        insights.append({
            "type": "pomodoro",
            "severity": SEVERITY["HIGH"],
            "text": (
                f"You worked continuously for about {longest_focus} minutes without a break. "
                "Using a Pomodoro rhythm (25 min focus, 5 min break) could help "
                "maintain energy and reduce fatigue."
            )
        })

    
    elif longest_focus >= 60:
        insights.append({
            "type": "pomodoro",
            "severity": SEVERITY["MEDIUM"],
            "text": (
                f"You had long focus sessions of around {longest_focus} minutes. "
                "Taking short breaks between focus blocks may help sustain productivity."
            )
        })

    return insights


def focus_blocks_rule(metrics):
    insights = []

    hourly = metrics.get("hourly_work", {})
    if not hourly:
        return insights

    
    filtered = {
        h: m for h, m in hourly.items()
        if 7 <= h <= 20 and m >= 30
    }

    if len(filtered) < 2:
        return insights

    
    avg_productive = sum(filtered.values()) / len(filtered)

    
    peak_hours = sorted(
        [h for h, m in filtered.items() if m >= avg_productive]
    )

    if not peak_hours:
        return insights

   
    blocks = []
    current = [peak_hours[0]]

    for h in peak_hours[1:]:
        if h == current[-1] + 1:
            current.append(h)
        else:
            blocks.append(current)
            current = [h]

    blocks.append(current)

    
    blocks = [b[:3] for b in blocks]

    
    def block_score(block):
        return sum(hourly[h] for h in block)

    best_block = max(blocks, key=block_score)

    start_hour = best_block[0]
    end_hour = best_block[-1] + 1

    insights.append({
        "type": "focus_blocks",
        "severity": "info",
        "text": (
            f"Your strongest focus window appears to be between "
            f"{start_hour}:00 and {end_hour}:00. "
            f"Scheduling deep-work or high-priority tasks during this period "
            f"may help you work more effectively."
        )
    })

    return insights

"""
def weekly_focus_blocks_rule(weekly_hourly, weekly_apps):
    insights = []

    # Filter realistic working hours
    filtered = {
        h: m for h, m in weekly_hourly.items()
        if 7 <= h <= 20 and m >= 120  # at least 2 hours across week
    }

    if len(filtered) < 2:
        return insights

    avg = sum(filtered.values()) / len(filtered)

    peak_hours = sorted(
        [h for h, m in filtered.items() if m >= avg]
    )

    if not peak_hours:
        return insights

    # Build continuous blocks
    blocks = []
    current = [peak_hours[0]]

    for h in peak_hours[1:]:
        if h == current[-1] + 1:
            current.append(h)
        else:
            blocks.append(current)
            current = [h]

    blocks.append(current)

    # Pick best block
    def block_score(block):
        return sum(filtered[h] for h in block)

    best_block = max(blocks, key=block_score)

    start_hour = best_block[0]
    end_hour = best_block[-1] + 1

    # Find most-used app in this block
    app_usage = {}
    for h in best_block:
        for app, dur in weekly_apps[h].items():
            app_usage[app] = app_usage.get(app, 0) + dur

    top_app = max(app_usage, key=app_usage.get)

    insights.append({
        "type": "weekly_focus_blocks",
        "severity": "info",
        "text": (
            f"Across the past week, your strongest recurring focus window was "
            f"between {start_hour}:00 and {end_hour}:00. During this period, "
            f"you spent the most focused time using {top_app}. Scheduling "
            f"high-priority or deep-work tasks in this window may help improve efficiency."
        )
    })

    return insights
"""

def weekly_focus_blocks_rule(weekly_hourly, weekly_apps):
    insights = []

    if not weekly_hourly:
        return insights

    
    filtered = {
        h: m for h, m in weekly_hourly.items()
        if 7 <= h <= 20 and m >= 120
    }

    if len(filtered) < 2:
        return insights

    
    WINDOW_SIZE = 2

    hours = sorted(filtered.keys())

    best_window = None
    best_score = 0

    
    for i in range(len(hours)):
        window = hours[i:i + WINDOW_SIZE]

        
        if len(window) < WINDOW_SIZE:
            continue

        
        if window[-1] != window[0] + WINDOW_SIZE - 1:
            continue

        score = sum(filtered[h] for h in window)

        if score > best_score:
            best_score = score
            best_window = window

    if not best_window:
        return insights

    start_hour = best_window[0]
    end_hour = start_hour + WINDOW_SIZE

    
    app_usage = {}

    for h in best_window:
        for app, dur in weekly_apps.get(h, {}).items():
            app_usage[app] = app_usage.get(app, 0) + dur

    top_app = max(app_usage, key=app_usage.get) if app_usage else "your primary work tools"

    insights.append({
        "type": "weekly_focus_blocks",
        "severity": "info",
        "text": (
            f"Across the past week, your strongest recurring focus window was "
            f"between {start_hour}:00 and {end_hour}:00. During this period, "
            f"you spent the most focused time using {top_app}. Scheduling "
            f"high-priority or deep-work tasks in this window may help improve efficiency."
        )
    })

    return insights
