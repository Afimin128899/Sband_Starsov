from aiogram import types
from loader import dp
from storage import user_balances, withdraw_requests

ADMINS = [123456789]

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@dp.message_handler(commands=["admin"])
async def admin_panel(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ У вас нет доступа к админ-панели.")
        return
    text = "👑 <b>Админ-панель Sband Stars</b>\n\nДоступные команды:\n/users - список пользователей и баланс\n/withdraws - заявки на вывод"
    await message.answer(text)

@dp.message_handler(commands=["users"])
async def admin_users(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    if not user_balances:
        await message.answer("Пока нет зарегистрированных пользователей.")
        return
    text = "👤 <b>Список пользователей и баланс:</b>\n\n"
    for uid, balance in user_balances.items():
        text += f"ID: <code>{uid}</code> — {balance} ⭐\n"
    await message.answer(text)

@dp.message_handler(commands=["withdraws"])
async def admin_withdraws(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    if not withdraw_requests:
        await message.answer("❌ Нет заявок на вывод.")
        return
    text = "💸 <b>Заявки на вывод:</b>\n\n"
    for wr in withdraw_requests:
        text += f"ID: <code>{wr['user_id']}</code> — {wr['amount']} ⭐ → {wr['target']} [{wr['status']}]\n"
    await message.answer(text)
