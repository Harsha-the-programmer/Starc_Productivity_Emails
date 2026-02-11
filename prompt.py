def build_pomodoro_prompt(user_name, date, metrics):
    productive_minutes = round(metrics.get("total_work_min", 0))
    longest_focus = round(metrics.get("longest_focus_min", 0))
    overwork_blocks = metrics.get("overwork_blocks", 0)

    return (
        f"You are a professional workplace productivity advisor.\n"
        f"Write a structured and supportive email addressed to {user_name}.\n\n"

        f"Email structure requirements:\n"
        f"- Include a clear subject line\n"
        f"- Start with a greeting addressing {user_name}\n"
        f"- End with a short professional closing sentence\n"
        f"- Keep the email between 140 and 180 words\n"
        f"- Tone should be professional, neutral, and supportive\n"
        f"- Do NOT mention tracking or monitoring\n"
        f"- Do NOT encourage longer working hours\n\n"

        f"Date: {date}\n\n"

        f"Facts that must be included accurately:\n"
        f"- Total productive time: {productive_minutes} minutes\n"
        f"- Longest continuous focus session: {longest_focus} minutes\n"
        f"- Number of extended sessions exceeding two hours: {overwork_blocks}\n\n"

        f"Instructions:\n"
        f"- Explicitly state the total productive minutes\n"
        f"- If extended sessions occurred, explain how structured short breaks "
        f"(for example, 25 minutes of focused work followed by a 5-minute break) "
        f"can support sustained focus and reduce mental fatigue\n"
        f"- Emphasize sustainable productivity rather than intensity\n"
        f"- Keep recommendations practical and realistic\n"
    )


def build_weekly_focus_prompt(user_name, week_range, start_hour, end_hour, top_app, window_minutes):
    return (
        f"You are a professional workplace productivity advisor.\n"
        f"Write a structured and constructive weekly insight email addressed to {user_name}.\n\n"

        f"Email structure requirements:\n"
        f"- Include a clear subject line\n"
        f"- Start with a greeting addressing {user_name}\n"
        f"- End with a short professional closing sentence\n"
        f"- Keep the email between 150 and 190 words\n"
        f"- Tone should be analytical, supportive, and practical\n"
        f"- Do NOT mention tracking or monitoring\n\n"

        f"Week Covered: {week_range}\n\n"

        f"Facts that must be included explicitly:\n"
        f"- Strongest recurring focus window: {start_hour}:00 to {end_hour}:00\n"
        f"- Total productive minutes in this window across the week: {round(window_minutes)}\n"
        f"- Most used productive tool during this period: {top_app}\n\n"

        f"Instructions:\n"
        f"- Clearly state the focus time window exactly as provided\n"
        f"- Suggest scheduling deep-work or high-priority tasks during this time range\n"
        f"- Keep advice concise and actionable\n"
        f"- Focus on efficiency and effectiveness rather than longer hours\n"
    )
