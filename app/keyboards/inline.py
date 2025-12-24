from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def task_buttons(signature: str):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="✅ Проверить выполнение", callback_data=f"check_{signature}"))
    return kb

def withdraw_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="💸 Создать заявку на вывод", callback_data="withdraw"))
    return kb

def ref_buttons(ref_link: str):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="🔗 Поделиться ссылкой", url=ref_link))
    return kb
