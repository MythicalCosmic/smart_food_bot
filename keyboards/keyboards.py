from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import get_translation
from utils.utils import get_category_name_all, get_subcategory_name_all, get_product_name_all
from database.models import SubCategory, Product


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

def generate_subcategory_keyboard(language: str) -> ReplyKeyboardMarkup:
    subcategory_str = get_subcategory_name_all(language)
    if not subcategory_str:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="No subcategories found")]],
            resize_keyboard=True
        )
    
    subcategories = [s.strip() for s in subcategory_str.split(",")]

    keyboard = []
    for i in range(0, len(subcategories), 2):  
        row = [KeyboardButton(text=subcategories[i])]
        if i + 1 < len(subcategories):
            row.append(KeyboardButton(text=subcategories[i + 1]))
        keyboard.append(row)

    back_text = get_translation("buttons.back", language) or "🔙 Back"
    keyboard.append([KeyboardButton(text=back_text)])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def generate_products_keyboard(language: str) -> ReplyKeyboardMarkup:
    product_names = get_product_name_all(language)
    if not product_names:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="No products found")]],
            resize_keyboard=True
        )

    keyboard = []
    for i in range(0, len(product_names), 2):
        row = [KeyboardButton(text=product_names[i])]
        if i + 1 < len(product_names):
            row.append(KeyboardButton(text=product_names[i + 1]))
        keyboard.append(row)

    basket_text = get_translation("buttons.basket", language) or "🛒 Basket"
    keyboard.append([KeyboardButton(text=basket_text)])


    back_text = get_translation("buttons.back", language) or "🔙 Back"
    keyboard.append([KeyboardButton(text=back_text)])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def generate_product_keyboard(product_id: int, language: str) -> InlineKeyboardMarkup:
    add_text = get_translation("buttons.add", language) or "➕ Add"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=add_text, callback_data=f"add:{product_id}")]
        ]
    )


def generate_quantity_keyboard(product_id: int, quantity: int, language: str) -> InlineKeyboardMarkup:
    texts = {
    "uz": {"minus": "➖", "plus": "➕", "count": f"{quantity}", "basket": "🛒 Savat"},
    "ru": {"minus": "➖", "plus": "➕", "count": f"{quantity}", "basket": "🛒 Корзина"},
    "en": {"minus": "➖", "plus": "➕", "count": f"{quantity}", "basket": "🛒 Basket"}
    }.get(language, {
    "minus": "➖", "plus": "➕", "count": f"{quantity}", "basket": "🛒 Basket"
    })


    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts["minus"], callback_data=f"decrease:{product_id}"),
                InlineKeyboardButton(text=texts["count"], callback_data="ignore"),
                InlineKeyboardButton(text=texts["plus"], callback_data=f"increase:{product_id}")
            ],
        ]
    )

def generate_quantity_only_keyboard(product_id: int, quantity: int) -> InlineKeyboardMarkup:
    """
    Generate only the plus/minus quantity control (without basket button).
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"decrease:{product_id}"),
                InlineKeyboardButton(text=str(quantity), callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data=f"increase:{product_id}")
            ]
        ]
    )

def generate_counter_keyboard(product_id: int, quantity: int) -> InlineKeyboardMarkup:
    """
    Generate a simple quantity counter keyboard: ➖ qty ➕
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"decrease:{product_id}"),
                InlineKeyboardButton(text=str(quantity), callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data=f"increase:{product_id}")
            ]
        ]
    )


