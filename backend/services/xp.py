def calculate_xp(correct: bool, time_left: int) -> int:
    if not correct:
        return 0
    return 10 + max(time_left, 0)
