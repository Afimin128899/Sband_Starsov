user_balances = {}
rewarded_users = set()
referrals = {}
withdraw_requests = []

def get_balance(user_id: int) -> float:
    return round(user_balances.get(user_id, 0), 2)

def set_balance(user_id: int, amount: float):
    user_balances[user_id] = round(amount, 2)
