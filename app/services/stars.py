from storage import user_balances, rewarded_users
from config import SUBSCRIBE_REWARD

def reward_subscription(user_id: int) -> bool:
    if user_id in rewarded_users:
        return False
    user_balances[user_id] = user_balances.get(user_id, 0) + SUBSCRIBE_REWARD
    rewarded_users.add(user_id)
    return True

def get_balance(user_id: int) -> float:
    return round(user_balances.get(user_id, 0), 2)
