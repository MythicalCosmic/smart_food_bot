from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import get_translation

UZ = "🇺🇿 O'zbek Tili"
RU = "🇷🇺 Русский язык"
EN = "🇺🇸 English"

def language_keys() -> ReplyKeyboardMarkup:
    
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=UZ)],
            [KeyboardButton(text=EN), KeyboardButton(text=RU)],
        ],
        resize_keyboard=True
    )

def menu_keys(language: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("buttons.order", language))],
            [
                KeyboardButton(text=get_translation("buttons.settings", language)),
                KeyboardButton(text=get_translation("buttons.about", language))
            ],
            [
                KeyboardButton(text=get_translation("buttons.sale", language)),
                KeyboardButton(text=get_translation("buttons.feedback", language))
            ],
            [KeyboardButton(text=get_translation("buttons.my_orders", language))]
        ],
        resize_keyboard=True
    )

def deliver_type_keys(language: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation('buttons.deliver', language=language)), KeyboardButton(text=get_translation("buttons.hand_deliver", language=language))],
            [KeyboardButton(text=get_translation("buttons.back", language=language))]
        ],
        resize_keyboard=True
    )

def location_keys(language: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("buttons.location", language=language), request_location=True), KeyboardButton(text=get_translation("buttons.back", language=language))]
        ],
        resize_keyboard=True
    )
