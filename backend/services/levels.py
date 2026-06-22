def calculate_level(total_xp: int) -> int:
    return max((total_xp // 100) + 1, 1)
