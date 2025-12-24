from aiogram import types
from loader import dp
from storage import referrals
from services.stars import get_balance
from config import BOT_USERNAME

@dp.message_handler(commands=["profile"])
async def profile_handler(message: types.Message):
    user = message.from_user
    balance = get_balance(user.id)
    ref_link = f"https://t.me/{BOT_USERNAME}?start=ref_{user.id}"
    invited_by = referrals.get(user.id)
    text = f"👤 <b>Профиль</b>\n\nID: <code>{user.id}</code>\nБаланс: <b>{balance} ⭐</b>\n🔗 Реферальная ссылка:\n{ref_link}"
    if invited_by:
        text += f"\n\n👥 Вас пригласил: <code>{invited_by}</code>"
    await message.answer(text)
