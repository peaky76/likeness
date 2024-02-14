def discount(calculation: float) -> float:
    if calculation < 0:
        raise ValueError("Discount function must return a value below 1")
    return max(1 - calculation, 0)
