def calculate_streak(current_streak: int, correct: bool) -> int:
    if not correct:
        return 0
    return current_streak + 1
