from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import get_translation
from utils.utils import get_category_name_all
from database.models import SubCategory


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

def cate_keys(language: str) -> ReplyKeyboardMarkup:
    category_str = get_category_name_all(language)
    if not category_str:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="No categories found")]],
            resize_keyboard=True
        )

    category_names = category_str.split(", ")

    keyboard = []
    for i in range(0, len(category_names), 2):
        row = [KeyboardButton(text=category_names[i])]
        if i + 1 < len(category_names):
            row.append(KeyboardButton(text=category_names[i + 1]))
        keyboard.append(row)


    back_text = get_translation("buttons.back", language) or "🔙 Back"
    keyboard.append([KeyboardButton(text=back_text)])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def settings_keys(language: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("buttons.language", language=language)),
             KeyboardButton(text=get_translation("buttons.birthday", language=language))],
            [KeyboardButton(text=get_translation("buttons.phone_number", language=language))],
            [KeyboardButton(text=get_translation("buttons.back", language=language))]
        ],
        resize_keyboard=True
    )

def generate_subcategory_keyboard(subcategories: list[SubCategory], language: str) -> ReplyKeyboardMarkup:
    name_field = f"name_{language}"

    keyboard = [
        [KeyboardButton(text=getattr(sub, name_field, sub.name_en or sub.name_uz or sub.name_ru))]
        for sub in subcategories
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
