from config import MIN_WITHDRAW

def is_valid_withdraw_amount(amount: float) -> bool:
    return amount >= MIN_WITHDRAW

def is_positive_float(value) -> bool:
    try:
        val = float(value)
        return val > 0
    except ValueError:
        return False
