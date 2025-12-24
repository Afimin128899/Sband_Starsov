from aiogram import types
from loader import dp
from storage import referrals
from services.stars import reward_subscription, get_balance
from config import BOT_USERNAME

@dp.message_handler(commands=["ref"])
async def ref_handler(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    ref_link = f"https://t.me/{BOT_USERNAME}?start=ref_{user_id}"
    invited_count = sum(1 for ref in referrals.values() if ref == user_id)
    text = f"👤 <b>Ваш профиль</b>\nБаланс: <b>{balance} ⭐</b>\n\n🔗 Ваша реферальная ссылка:\n{ref_link}\n👥 Приглашено пользователей: {invited_count}"
    await message.answer(text)

@dp.message_handler(commands=["claim_ref"])
async def claim_ref_handler(message: types.Message):
    user_id = message.from_user.id
    for uid, referrer_id in referrals.items():
        if uid == user_id:
            rewarded = reward_subscription(referrer_id)
            balance = get_balance(referrer_id)
            if rewarded:
                await message.answer(f"🎉 Ваш реферал выполнил подписку! {referrer_id} получил 0.25 ⭐\n💰 Баланс: {balance} ⭐")
            else:
                await message.answer("✅ Награда за реферала уже была начислена.")
            return
    await message.answer("❌ Нет данных о приглашении.")
