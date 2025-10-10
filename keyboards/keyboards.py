from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config.settings import get_translation
from utils.utils import get_category_name_all, get_subcategory_name_all, get_product_name_all, get_subcategories_by_category_id, get_products_by_subcategories_id
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
    keyboard.append([KeyboardButton(text=get_translation("web_app", language), web_app=WebAppInfo(url="https://e1f355430a5d.ngrok-free.app"))])

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

def generate_subcategory_keyboard(language: str, category_id: int) -> ReplyKeyboardMarkup:
    # Get only subcategories for this specific category
    subcategories = get_subcategories_by_category_id(category_id)
    
    if not subcategories:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="No subcategories found")]],
            resize_keyboard=True
        )
    
    # Get the correct name based on language
    subcategory_names = [getattr(sub, f'name_{language}') for sub in subcategories]

    keyboard = []
    for i in range(0, len(subcategory_names), 2):  
        row = [KeyboardButton(text=subcategory_names[i])]
        if i + 1 < len(subcategory_names):
            row.append(KeyboardButton(text=subcategory_names[i + 1]))
        keyboard.append(row)

    back_text = get_translation("buttons.back", language) or "🔙 Back"
    keyboard.append([KeyboardButton(text=back_text)])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# FIXED: Now accepts subcategory_id and filters products
def generate_products_keyboard(language: str, subcategory_id: int) -> ReplyKeyboardMarkup:
    # Get only products for this specific subcategory
    products = get_products_by_subcategories_id(subcategory_id)
    
    if not products:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="No products found")]],
            resize_keyboard=True
        )

    product_names = [getattr(prod, f'name_{language}') for prod in products]

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
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"decrease:{product_id}"),
                InlineKeyboardButton(text=str(quantity), callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data=f"increase:{product_id}")
            ]
        ]
    )

def generate_accept_keyboard(language: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_translation("confirm", language), callback_data="confirm_order")],
            [InlineKeyboardButton(text=get_translation("cancel", language), callback_data="cancel_order")],
        ]
    )
    return keyboard

def generate_payment_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"💵 {get_translation('payment_cash', language)}",
                    callback_data="payment_cash"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"💸 {get_translation('payment_click', language)}",
                    callback_data="payment_click"
                ),
                InlineKeyboardButton(
                    text=f"💰 {get_translation('payment_payme', language)}",
                    callback_data="payment_payme"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"⬅️ {get_translation('back', language)}",
                    callback_data="payment_back"
                ),
            ]
        ]
    )

def purchase_button(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_translation('buy', language), pay=True)]
        ]
    )

def admin_buttons(language: str, user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"order_confirm:{user_id}"),
            InlineKeyboardButton(text="🚚 Yetkazildi", callback_data=f"order_delivered:{user_id}")
        ],
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"order_cancel:{user_id}")
        ]
    ])