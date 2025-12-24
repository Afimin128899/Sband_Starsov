import asyncio
from aiogram import Bot, Dispatcher, types, executor
from flyerapi import Flyer

API_TOKEN = "8389664932:AAHw-vE5o52ODbQgUPcHf5CsSlhAIls_vDE"       # Ваш токен Telegram-бота
FLYER_API_KEY = "FL-JCQcno-ZEliXE-fQqxRr-rfbkQS"     # API ключ FlyerAPI

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

flyer = Flyer(FLYER_API_KEY)

# Главное меню (Reply Keyboard)
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Задания", "Профиль")
    return keyboard

# Кнопка Назад (Reply Keyboard)
def back_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Назад")
    return keyboard

# /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=main_menu())

# Показ заданий
@dp.message_handler(lambda m: m.text == "Задания")
async def show_tasks(message: types.Message):
    user_id = message.from_user.id
    language_code = message.from_user.language_code

    tasks = await flyer.get_tasks(user_id=user_id, language_code=language_code, limit=5)
    if not tasks:
        await message.answer("Нет доступных заданий.", reply_markup=back_button())
        return

    for task in tasks:
        signature = task.get("signature")

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            text="Отметить выполненным", callback_data=f"mark_{signature}"
        ))

        text = f"📌 {task.get('title', 'Без названия')}\n{task.get('description', '')}"
        await message.answer(text, reply_markup=keyboard)

    await message.answer("Нажмите Назад для возврата в меню", reply_markup=back_button())

# Отметка задания как выполненного
@dp.callback_query_handler(lambda c: c.data.startswith("mark_"))
async def mark_task(call: types.CallbackQuery):
    signature = call.data.replace("mark_", "")
    user_id = call.from_user.id

    status = await flyer.check_task(user_id=user_id, signature=signature)
    if status and status.get("status") == "completed":
        await call.answer("Задание подтверждено выполненным 👍", show_alert=True)
    else:
        await call.answer("Задание ещё не выполнено 😕", show_alert=True)

# Профиль пользователя
@dp.message_handler(lambda m: m.text == "Профиль")
async def profile_handler(message: types.Message):
    user_id = message.from_user.id
    tasks = await flyer.get_tasks(user_id=user_id, language_code=message.from_user.language_code, limit=50)
    completed = sum(1 for t in tasks if t.get("completed")) if tasks else 0

    text = (
        f"Профиль:\n"
        f"Пользователь: {message.from_user.full_name}\n"
        f"Выполненные задания: {completed}"
    )
    await message.answer(text, reply_markup=back_button())

# Назад в главное меню
@dp.message_handler(lambda m: m.text == "Назад")
async def back_handler(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    
