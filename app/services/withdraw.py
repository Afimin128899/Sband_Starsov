from storage import user_balances, withdraw_requests
from config import MIN_WITHDRAW

def create_withdraw_request(user_id: int, amount: float, target: str):
    balance = user_balances.get(user_id, 0)
    if amount < MIN_WITHDRAW or balance < amount:
        return False, "Недостаточно ⭐ или сумма меньше минимума"
    user_balances[user_id] -= amount
    withdraw_requests.append({
        "user_id": user_id,
        "amount": round(amount, 2),
        "target": target,
        "status": "pending"
    })
    return True, "Заявка создана"
