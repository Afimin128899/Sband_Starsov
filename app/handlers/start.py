from aiogram import types
from loader import dp
from services.flyer import check_subscription
from services.stars import reward_subscription, get_balance
from storage import referrals
from config import BOT_USERNAME

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    args = message.get_args()
    user = message.from_user
    if args.startswith("ref_"):
        try:
            referrer_id = int(args.replace("ref_", ""))
            if referrer_id != user.id:
                referrals[user.id] = referrer_id
        except ValueError:
            pass
    subscribed = await check_subscription(user)
    if not subscribed:
        return
    rewarded = reward_subscription(user.id)
    balance = get_balance(user.id)
    text = "✅ Подписка подтверждена\n"
    if rewarded:
        text += "🎉 Вы получили 0.25 ⭐\n"
    text += f"\n💰 Баланс: {balance} ⭐"
    await message.answer(text)
