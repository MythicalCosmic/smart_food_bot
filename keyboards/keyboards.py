from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import get_translation
from utils.utils import get_category_name_all

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

def location_keys(language: str = "uz", saved_location: str | None = None) -> ReplyKeyboardMarkup:
    if saved_location:
        keyboard = [
            [KeyboardButton(text=saved_location)],
            [KeyboardButton(text=get_translation("buttons.location", language=language), request_location=True)],
            [KeyboardButton(text=get_translation("buttons.back", language=language))]
        ]
    else:
        keyboard = [
            [KeyboardButton(text=get_translation("buttons.location", language=language), request_location=True)],
            [KeyboardButton(text=get_translation("buttons.back", language=language))]
        ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def location_confirmation_keys(language: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("buttons.confirm", language=language)),KeyboardButton(text=get_translation("buttons.resend", language=language))],
            [KeyboardButton(text=get_translation("buttons.add_more", language=language)), KeyboardButton(text=get_translation("buttons.back", language=language))]
        ],
        resize_keyboard=True
    )

def cate_keys() -> ReplyKeyboardMarkup:
    category_str = get_category_name_all()
    if not category_str:
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="No categories found")]], resize_keyboard=True)

    category_names = category_str.split(", ")

    keyboard = [[KeyboardButton(text=name)] for name in category_names]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)