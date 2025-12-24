import logging
from aiogram import executor
from loader import dp, bot
from keyboards.main import main_keyboard
from storage import user_balances

from handlers import start, profile, withdraw, tasks, referral, admin

logging.basicConfig(level=logging.INFO)

@dp.message_handler(lambda message: message.text in ["👤 Профиль", "📋 Задания", "💸 Вывод", "🔗 Реферальная ссылка"])
async def main_menu_handler(message):
    if message.text == "👤 Профиль":
        await profile.profile_handler(message)
    elif message.text == "📋 Задания":
        await tasks.tasks_handler(message)
    elif message.text == "💸 Вывод":
        await withdraw.withdraw_handler(message)
    elif message.text == "🔗 Реферальная ссылка":
        await referral.ref_handler(message)

@dp.message_handler(commands=["menu"])
async def menu(message):
    await message.answer("Выберите действие:", reply_markup=main_keyboard)

@dp.message_handler()
async def unknown(message):
    await message.answer("❌ Неизвестная команда. Используйте главное меню или /menu.", reply_markup=main_keyboard)

if __name__ == "__main__":
    logging.info("Sband Stars Bot запущен!")
    executor.start_polling(dp, skip_updates=True)
