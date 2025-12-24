from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btn_profile = KeyboardButton("👤 Профиль")
btn_tasks = KeyboardButton("📋 Задания")
btn_withdraw = KeyboardButton("💸 Вывод")
btn_ref = KeyboardButton("🔗 Реферальная ссылка")
main_keyboard.add(btn_profile, btn_tasks)
main_keyboard.add(btn_withdraw, btn_ref)
