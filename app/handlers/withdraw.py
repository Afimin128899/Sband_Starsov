from aiogram import types
from loader import dp
from services.withdraw import create_withdraw_request

@dp.message_handler(commands=["withdraw"])
async def withdraw_handler(message: types.Message):
    args = message.get_args().split()
    if len(args) < 2:
        await message.answer("❌ Формат: /withdraw сумма способ")
        return
    try:
        amount = float(args[0])
    except ValueError:
        await message.answer("❌ Неверная сумма")
        return
    target = args[1]
    user_id = message.from_user.id
    success, text = create_withdraw_request(user_id, amount, target)
    await message.answer(f"{'✅' if success else '❌'} {text}")
