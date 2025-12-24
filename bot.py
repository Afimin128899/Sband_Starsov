import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from flyerapi import Flyer
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
FLYER_KEY = os.getenv("FLYER_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Инициализация Flyer API клиента
flyer = Flyer(FLYER_KEY)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот с заданиями.\n"
        "Нажми /tasks чтобы получить задания."
    )

@dp.message_handler(commands=["tasks"])
async def send_tasks(message: types.Message):
    user_id = message.from_user.id
    language = message.from_user.language_code or "en"

    # Получаем задания через Flyer API
    try:
        tasks = await flyer.get_tasks(user_id=user_id, language_code=language, limit=5)
    except Exception as e:
        logging.error(f"Error fetching tasks: {e}")
        await message.reply("Ошибка при получении заданий.")
        return

    if not tasks:
        await message.reply("Заданий нет 😕 Попробуй позже.")
        return

    keyboard = InlineKeyboardMarkup(row_width=1)

    # Создаем кнопки для каждого задания
    for t in tasks:
        sig = t.get("signature")
        desc = t.get("text", "Задание")
        btn = InlineKeyboardButton(
            text=f"Выполнить: {desc[:30]}...",
            callback_data=f"task_{sig}"
        )
        keyboard.add(btn)

    await message.answer("Выбери задание:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("task_"))
async def handle_task_click(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    signature = callback.data.split("_", 1)[1]

    await bot.answer_callback_query(callback.id)

    # Проверка статуса задания
    try:
        status = await flyer.check_task(user_id=user_id, signature=signature)
    except Exception as e:
        logging.error(f"Error checking task status: {e}")
        await bot.send_message(user_id, "Не удалось проверить задание.")
        return

    # Статус может возвращать словарь с info о выполнении
    done = status.get("done", False)
    reward = status.get("reward", 0)

    if done:
        await bot.send_message(user_id, f"✔️ Задание выполнено! Награда: {reward}")
    else:
        await bot.send_message(user_id, "🕒 Задание ещё не выполнено. Попробуй позже.")

@dp.message_handler()
async def fallback(message: types.Message):
    await message.reply("Используйте /tasks чтобы получить задания.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
