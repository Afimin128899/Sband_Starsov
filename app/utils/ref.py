from storage import referrals

def make_ref_link(user_id: int, bot_username: str) -> str:
    return f"https://t.me/{bot_username}?start=ref_{user_id}"

def count_invited(user_id: int) -> int:
    return sum(1 for ref in referrals.values() if ref == user_id)
