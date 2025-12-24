from loader import dp
from services.flyer import flyer
from services.stars import reward_subscription, get_balance
from aiogram import types

@dp.message_handler(commands=["tasks"])
async def tasks_handler(message: types.Message):
    user = message.from_user
    tasks = await flyer.get_tasks(user_id=user.id, language_code=user.language_code, limit=5)
    if not tasks["result"]:
        await message.answer("❌ Нет доступных заданий")
        return
    text = "📋 <b>Ваши задания:</b>\n\n"
    for idx, task in enumerate(tasks["result"], start=1):
        task_desc = task.get("description") or str(task)
        text += f"{idx}. {task_desc}\n"
    await message.answer(text)

@dp.message_handler(commands=["check_task"])
async def check_task_handler(message: types.Message):
    user = message.from_user
    args = message.get_args().split()
    if not args:
        await message.answer("❌ Формат: /check_task signature")
        return
    signature = args[0]
    status = await flyer.check_task(signature=signature)
    result = status.get("result")
    if result == "completed":
        rewarded = reward_subscription(user.id)
        balance = get_balance(user.id)
        text = f"✅ Задание выполнено!\n"
        if rewarded:
            text += "🎉 Вы получили 0.25 ⭐\n"
        text += f"💰 Баланс: {balance} ⭐"
    else:
        text = "❌ Задание ещё не выполнено или не найдено"
    await message.answer(text)
