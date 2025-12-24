from flyerapi import Flyer
from config import FLYER_KEY

flyer = Flyer(FLYER_KEY)

async def check_subscription(user):
    message = {
        "rows": 2,
        "text": "<b>Sband Stars</b>\n🎁 Подпишитесь, чтобы получить 0.25 ⭐",
        "button_channel": "Подписаться",
        "button_bot": "Проверить"
    }
    return await flyer.check(user_id=user.id, language_code=user.language_code, message=message)
