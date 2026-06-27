def calculate_badges(existing_badges: str, score_percentage: int) -> str:
    badges = {badge for badge in existing_badges.split(",") if badge}
    if score_percentage >= 100:
        badges.add("Perfect Score")
    elif score_percentage >= 80:
        badges.add("High Scorer")
    elif score_percentage >= 60:
        badges.add("Good Effort")
    return ",".join(sorted(badges))
