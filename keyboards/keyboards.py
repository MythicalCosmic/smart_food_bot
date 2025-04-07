from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


UZ = "Ozbek Tili"
RU = "Русский язык"
EN = "Ingliz tili"
ORDER = "ORDER"

def language_keys() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=UZ)],
            [KeyboardButton(text=EN), KeyboardButton(text=RU)],
        ],
        resize_keyboard=True
    )

def menu_keys() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ORDER)]
        ],
        resize_keyboard=True
    )