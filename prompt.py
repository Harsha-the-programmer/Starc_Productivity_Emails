"""
def build_prompt(user_name, date, metrics, insights):
    longest_focus = round(metrics.get("longest_focus_min", 0))

    if insights:
        insight_text = "\n".join(f"- {i['text']}" for i in insights)
    else:
        insight_text = "- Your work pattern looked balanced with healthy breaks."

    has_pomodoro = any(i["type"] == "pomodoro" for i in insights)

    pomodoro_hint = (
        "Briefly explain how using short focus cycles and regular breaks "
        "(such as the Pomodoro technique: 25 minutes work, 5 minutes break) "
        "can help maintain energy and productivity.\n\n"
        if has_pomodoro
        else ""
    )

    return (
        f"You are a practical productivity coach focused on healthy work habits.\n"
        f"Write a short, clear, and supportive email to {user_name}.\n\n"

        f"IMPORTANT RULES:\n"
        f"- Do NOT praise long working hours\n"
        f"- Do NOT encourage working longer\n"
        f"- Do NOT include a subject line\n"
        f"- Do NOT include regards, sign-offs, or your name\n"
        f"- Do NOT mention monitoring, tracking, rules, or severity levels\n"
        f"- Keep the tone neutral, calm, and informative\n\n"

        f"Keep the email under 120 words.\n\n"

        f"Date: {date}\n\n"

        f"Observation:\n"
        f"- A continuous focus session of {longest_focus} minutes was observed.\n\n"

        f"Recommendation:\n"
        f"{insight_text}\n\n"

        f"{pomodoro_hint}"
        f"End with a neutral, supportive closing sentence without any sign-off."
    )

"""

from metrics import productivity_summary


def build_prompt(user_name, date, metrics, insights, weekly_focus_text=None, weekly_productive_minutes=None):
    longest_focus = round(metrics.get("longest_focus_min", 0))
    productivity_text = productivity_summary(metrics)
    productive_minutes = round(metrics.get("total_work_min", 0))

    insight_text = (
        "\n".join(f"- {i['text']}" for i in insights)
        if insights
        else "- No major focus issues were observed."
    )

    weekly_productivity_block = ""

    if weekly_productive_minutes:
        weekly_productivity_block = (
            f"\nMANDATORY WEEKLY OBSERVATION:\n"
            f"- Across the past week, you spent approximately "
            f"{weekly_productive_minutes} minutes on productive work.\n\n"
            f"IMPORTANT:\n"
            f"- You MUST include this weekly productivity number explicitly\n"
            f"- Do NOT generalize it\n\n"
        )


    focus_block_section = ""
    if weekly_focus_text:
        focus_block_section = (
            f"\nMANDATORY OBSERVATION:\n"
            f"- {weekly_focus_text}\n\n"
            f"IMPORTANT:\n"
            f"- You MUST include this focus time window explicitly in the email\n"
            f"- Do NOT generalize it\n\n"
        )

    

    return (
        f"You are a practical productivity coach focused on sustainable work habits.\n"
        f"Write a short, clear, and supportive email to {user_name}.\n\n"

        f"IMPORTANT RULES:\n"
        f"- Do NOT praise long working hours\n"
        f"- Do NOT encourage working longer\n"
        f"- Do NOT include a subject line\n"
        f"- Do NOT include regards, sign-offs, or names\n"
        f"- Do NOT mention monitoring or tracking\n"
        f"- Keep tone neutral and informative\n\n"

        f"Keep the email under 120 words.\n\n"

        f"Date: {date}\n\n"

        f"MANDATORY REQUIREMENT:\n"
        f"- The email MUST explicitly include this sentence (you may rephrase slightly, "
        f"but the numbers must remain the same):\n"
        f"  \"You spent approximately {productive_minutes} minutes on productive work during the day.\"\n\n"


        f"Observations:\n"
        f"- You spent approximately {productive_minutes} minutes on productive work during the day.\n"
        f"- Longest uninterrupted focus session: {longest_focus} minutes\n"
        f"{weekly_productivity_block}"
        f"{focus_block_section}"


        f"IMPORTANT:\n"
        f"- You MUST explicitly mention the total productive minutes\n"
        f"- Do NOT generalize productivity without referencing the numbers above\n\n"

        f"Recommendation:\n"
        f"{insight_text}\n\n"

        f"Address BOTH of the following points clearly:\n"
        f"1. Explain how structuring work into short focus blocks with breaks "
        f"(for example, the Pomodoro technique: 25 minutes work, 5 minutes break) "
        f"can improve sustained focus and reduce mental fatigue.\n"
        f"2. Explain how being mindful of productive vs non-productive time "
        f"can help improve overall work effectiveness without increasing work hours.\n\n"

        f"End with a neutral, supportive closing sentence."
    )
