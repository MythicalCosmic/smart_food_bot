from aiogram import Router, Bot, F
from aiogram.types import Message, ContentType, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from .states import UserStates, OrderStates
from config.settings import get_translation, get_button_text
from keyboards.keyboards import *
from utils.utils import *
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from aiogram.types import CallbackQuery

router = Router()


@router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        if user_exists(user_id=user_id) and language is not None:
            await message.reply(get_translation('menu_message', language=language), reply_markup=menu_keys(language=language), parse_mode="HTML")
            await state.set_state(UserStates.menu)
            set_user_state(user_id=user_id, state=UserStates.menu.state)
        else:
            await message.reply(get_translation('start_text', 'uz'), reply_markup=language_keys(), parse_mode="HTML")
            await state.set_state(UserStates.set_language)
    except Exception as e:
        await message.reply(f"Error occured in start handler: {e}")

@router.message(lambda message: message.text in [EN, RU, UZ], StateFilter(UserStates.set_language))
async def set_language_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language_map = {
            "🇺🇸 English": "en",
            "🇺🇿 O'zbek Tili": "uz",
            "🇷🇺 Русский язык": "ru" 
        }
        language = language_map.get(message.text, "ru")
        set_user_state(user_id=user_id, state=UserStates.set_language.state)
        set_language_user(user_id=user_id, language=language)
        user_language = get_user_language(user_id=user_id)
        await message.reply(get_translation('menu_message', user_language), reply_markup=menu_keys(user_language), parse_mode="HTML")
        set_user_state(user_id=user_id, state=UserStates.menu.state)
        await state.set_state(UserStates.menu)
    except Exception as e:
        await message.reply(f'Error occurred: {e}')

@router.message(lambda message: message.text == get_button_text('order', get_user_language(message.from_user.id)), StateFilter(UserStates.menu))
async def order_handler(message: Message, state: FSMContext, bot: Bot):    
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=OrderStates.type.state)
        await message.reply(get_translation("type", language=language), parse_mode="HTML", reply_markup=deliver_type_keys(language=language))
        await state.set_state(OrderStates.type)
    except Exception as e:
        await message.reply(f"Error occured: {e}")

@router.message(lambda message: message.text == get_button_text('settings', get_user_language(message.from_user.id)), StateFilter(UserStates.menu))
async def settings_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        await message.reply(get_translation("settings_message", language=language), parse_mode="HTML", reply_markup=settings_keys(language=language))
        set_user_state(user_id=user_id, state=UserStates.menu.state)
        await state.set_state(UserStates.menu)
    except Exception as e:
        await message.reply(f"Error occured: {e}")

@router.message(lambda message: message.text == get_button_text('hand_deliver', get_user_language(message.from_user.id)), StateFilter(OrderStates.type))
async def order_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=OrderStates.items.state)
        await message.reply(
            text=get_translation("items_message", language=language),
            parse_mode="HTML", reply_markup=cate_keys(language=language)
        )
        await state.set_state(OrderStates.items)
    except Exception as e:
        await message.reply(f"Error occured: {e}")

@router.message(lambda message: message.text == get_button_text("deliver", get_user_language(message.from_user.id)), StateFilter(OrderStates.type))
async def handle_auto_deliver(message: Message, state: FSMContext, bot: Bot):
    
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        user_location = get_user_location(user_id)
        set_user_state(user_id=user_id, state=OrderStates.location.state)
        add_user_order_type(user_id=user_id, order_type="deliver")
        await message.reply(get_translation("location", language=language), parse_mode="HTML", reply_markup=location_keys(language=language, saved_location=user_location))
        await state.set_state(OrderStates.location)
    except Exception as e:
        await message.reply(f"Error occured: {e}")

@router.message(F.content_type == ContentType.LOCATION, StateFilter(OrderStates.location))
async def handle_location(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        latitude = message.location.latitude
        longitude = message.location.longitude

        set_user_state(user_id=user_id, state=OrderStates.location_confirmation.state)
        add_user_location(user_id=user_id, latitude=latitude, longitude=longitude)
        geolocator = Nominatim(user_agent="my_telegram_bot")
        try:
            location = geolocator.reverse((latitude, longitude), timeout=10)
            address = location.address if location else "Unknown location"
        except GeocoderTimedOut:
            address = "Address lookup timed out"
        await message.reply(
           get_translation("location_confirmation", language=language).replace("{location}", address),
            parse_mode="HTML", reply_markup=location_confirmation_keys(language=language)
        )
        await state.set_state(OrderStates.location_confirmation)
    except Exception as e:
        await message.reply(f"⚠️ Error occurred: {e}")

@router.message(
    lambda message: message.text == get_button_text("confirm", get_user_language(message.from_user.id)),
    StateFilter(OrderStates.location_confirmation)
)
async def confirm_location(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        
        user_location = get_user_location(user_id=user_id) or ""
        extra_location = get_user_extra_location(user_id=user_id) or ""

        set_user_state(user_id=user_id, state=OrderStates.items.state)

        await message.reply(
            text=get_translation("location_confirmed", language=language).replace("{location}", str(user_location))
                 + (f"\n\n{extra_location}" if extra_location else ""),
            parse_mode="HTML",
        )

        await message.reply(
            text=get_translation("items_message", language=language),
            parse_mode="HTML",
            reply_markup=cate_keys(language=language)
        )

        await state.set_state(OrderStates.items)

    except Exception as e:
        await message.reply(f"Error occurred: {e}")


@router.message(lambda message: message.text == get_button_text("resend", get_user_language(message.from_user.id)), StateFilter(OrderStates.location_confirmation))
async def resend_location(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=OrderStates.location.state)
        user_location = get_user_location(user_id=user_id)
        await message.reply(
            text=get_translation("location", language=language),
            parse_mode="HTML", reply_markup=location_keys(language=language, saved_location=user_location)
        )
        await state.set_state(OrderStates.location)
    except Exception as e:
        await message.reply(f"Error occurred: {e}")

@router.message(lambda message: message.text == get_button_text("add_more", get_user_language(message.from_user.id)), StateFilter(OrderStates.location_confirmation))
async def add_more_location(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=OrderStates.location.state)
        await message.reply(
            text=get_translation("extra_location_text", language=language),
            parse_mode="HTML"
        )
        await state.set_state(OrderStates.extra_location)
    except Exception as e:
        await message.reply(f"Error occurred: {e}")

@router.message(StateFilter(OrderStates.extra_location))
async def handle_extra_location(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        extra_location = message.text.strip()
        add_user_extra_location(user_id=user_id, extra_location=extra_location)
        if extra_location:
            set_user_state(user_id=user_id, state=OrderStates.location_confirmation.state)
            await message.reply(
                text=get_translation("extra_location_confirmed", language=language).replace("{extra_location}", extra_location).replace("{location}", get_user_location(user_id=user_id)),
                parse_mode="HTML", reply_markup=location_confirmation_keys(language=language)
            )
            await state.set_state(OrderStates.location_confirmation)
        else:
            await message.reply(get_translation("empty_location_error", language=language), parse_mode="HTML")
    except Exception as e:
        await message.reply(f"Error occurred: {e}")


@router.message(lambda message: any(word in message.text.lower() for word in ["andijon", "o'zbekiston", "marhamat"]), StateFilter(OrderStates.location))
async def handle_items(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=OrderStates.items.state)
        user_location = message.text
        await message.reply(
            text=get_translation("location_confirmed", language=language).replace("{location}", user_location),
            parse_mode="HTML", reply_markup=cate_keys(language=language)
        )
        await state.set_state(OrderStates.items)
    except Exception as e:
        await message.reply(f"Error occured: {e}")

@router.message(lambda message: message.text == get_button_text("basket", get_user_language(message.from_user.id)), StateFilter(OrderStates.products))
async def handle_basket_button(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    basket_text = get_translation("buttons.basket", language) or "🛒 Basket"
    if message.text != basket_text:
        return 

    basket_items = get_user_basket(user_id) 
    if not basket_items:
        await message.reply(
            text=get_translation("basket_empty", language) or "🛒 Your basket is empty!",
            parse_mode="HTML",
            reply_markup=generate_products_keyboard(language)
        )
        return

    lines = []
    total_price = 0
    for item in basket_items:
        product = get_product_by_id(item.product_id)
        product_name = getattr(product, f"name_{language}", product.name_en)
        item_total = product.price * item.quantity
        total_price += item_total
        lines.append(f"• <b>{product_name}</b> × {item.quantity} = {item_total} UZS")

    basket_summary = "\n".join(lines)
    basket_summary += f"\n\n<b>{get_translation('total', language) or 'Total'}:</b> {total_price} UZS"

    base_lat, base_lon = 40.494433, 72.325357

    user_lat, user_lon = get_user_latlon(user_id)  

    distance_km = calculate_distance(base_lat, base_lon, user_lat, user_lon)

    delivery_cost = 5000
    if distance_km > 1:
        delivery_cost += int((distance_km - 1) * 1000)

    total_with_delivery = total_price + delivery_cost

    basket_summary = "\n".join(lines)
    basket_summary += f"\n\n🚚 <b>Delivery:</b> {delivery_cost} UZS"
    basket_summary += f"\n<b>{get_translation('total', language) or 'Total'}:</b> {total_with_delivery} UZS"

    await message.reply(
        text=f"<b>{get_translation('your_basket', language) or 'Your Basket'}</b>\n\n{basket_summary}",
        parse_mode="HTML",
        reply_markup=generate_products_keyboard(language) 
    )



@router.message(StateFilter(UserStates.menu))
async def menu_handler(message: Message, state: FSMContext, bot: Bot):
    
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        await message.reply(get_translation('menu_message', language=language), reply_markup=menu_keys(language=language), parse_mode="HTML")
        set_user_state(user_id=user_id, state=UserStates.menu.state)
    except Exception as e:
        await message.reply(f"Error occured: {e}")

@router.message(lambda message: message.text == get_button_text("back", get_user_language(message.from_user.id)), StateFilter(OrderStates.type, OrderStates.location, OrderStates.location_confirmation, OrderStates.items, OrderStates.subcategory, OrderStates.products))
async def handle_centeral_back(message: Message, state: FSMContext, bot: Bot):
    try:
        current_state = await state.get_state()
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        user_location = get_user_location(user_id=user_id)

        async def go_to_main_menu():
            await state.set_state(UserStates.menu)  
            set_user_state(user_id, UserStates.menu.state) 
            await message.answer(                      
                get_translation("menu_message", language=language),
                reply_markup=menu_keys(language=language),
                parse_mode="HTML"
            )
        async def go_to_order_type():
            await state.set_state(OrderStates.type)
            set_user_state(user_id, OrderStates.type.state)
            await message.answer(get_translation("type", language=language), reply_markup=deliver_type_keys(language=language), parse_mode="HTML")
        
        async def go_to_location():
            await state.set_state(OrderStates.location)
            set_user_state(user_id=user_id, state=OrderStates.location.state)
            await message.answer(get_translation("location", language=language), reply_markup=location_keys(language=language, saved_location=user_location), parse_mode="HTML")

        async def go_to_location_confirmation():
            await state.set_state(OrderStates.location_confirmation)
            set_user_state(user_id=user_id, state=OrderStates.location_confirmation.state)
            user_location = get_user_location(user_id=user_id)
            await message.answer(
                get_translation("location_confirmation", language=language).replace("{location}", user_location),
                reply_markup=location_confirmation_keys(language=language),
                parse_mode="HTML"
            )
        async def  go_to_items():
            await state.set_state(OrderStates.items)
            set_user_state(user_id=user_id, state=OrderStates.items.state)
            await message.answer(get_translation("items_message", language=language), reply_markup=cate_keys(language=language),
                                  parse_mode="HTML")
            
        async def go_to_subcategory():
            await state.set_state(OrderStates.subcategory)
            set_user_state(user_id=user_id, state=OrderStates.subcategory.state)
            await message.answer(get_translation("subcategory_message", language=language), reply_markup=cate_keys(language=language),
                                  parse_mode="HTML")
            
        async def go_to_products():
            await state.set_state(OrderStates.products)
            set_user_state(user_id=user_id, state=OrderStates.products.state)
            await message.answer(get_translation("products_message", language=language), reply_markup=cate_keys(language=language),
                                  parse_mode="HTML")
        state_actions = {
            OrderStates.type.state: go_to_main_menu,
            OrderStates.location.state: go_to_order_type,
            OrderStates.location_confirmation: go_to_location,
            OrderStates.items.state: go_to_location_confirmation,
            OrderStates.subcategory.state: go_to_items,
            OrderStates.products.state: go_to_subcategory,
        }

        action = state_actions.get(current_state)
        if action:
            await action()
        else:
            await message.answer("Unknown state. Please try again.")

    except Exception as e:
        await message.reply(f"Error occurred: {e}")

@router.message(StateFilter(OrderStates.items))
async def handle_category_selection(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_user_language(user_id)
    selected_category_name = message.text
    try:
        category = get_category_by_name(selected_category_name, language)
        if not category:  
            await message.reply(
                text=get_translation("category_not_found", language=language).replace("{name}", selected_category_name),
                parse_mode="HTML",
                reply_markup=cate_keys(language=language) 
            )
            return
        subcategories = get_subcategories_by_category_id(category.id)
        if not subcategories: 
            await message.reply(
                text=get_translation("no_subcategories", language=language).replace("{name}", selected_category_name),
                parse_mode="HTML",
                reply_markup=cate_keys(language=language)
            )
            return
        keyboard = generate_subcategory_keyboard(language)

        await message.reply(
            text=get_translation("subcategory_message", language=language),
            parse_mode="HTML",
            reply_markup=keyboard
        )
        set_user_state(user_id=user_id, state=OrderStates.subcategory.state)
        await state.set_state(OrderStates.subcategory)

    except Exception as e:
        await message.reply(f"❌ Error on Items: {e}")


@router.message(StateFilter(OrderStates.subcategory))
async def handle_subcategory_selection(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    language = get_user_language(user_id)
    selected_subcategory_name = message.text
    try:
        subcategory = get_subcategory_by_name(selected_subcategory_name, language)
        if not subcategory:  
            await message.reply(
                text=get_translation("subcategory_not_found", language=language).replace("{name}", selected_subcategory_name),
                parse_mode="HTML",
                reply_markup=generate_subcategory_keyboard(language=language) 
            )
            return
        
        products = get_products_by_subcategories_id(subcategory.id)
        if not products:
            await message.reply(
                text=get_translation("no_products", language=language),
                parse_mode="HTML",
                reply_markup=generate_subcategory_keyboard(language=language)
            )
            return


        keyboard = generate_products_keyboard(language)
        await message.reply(
            text=get_translation("products_message", language=language),
            parse_mode="HTML",
            reply_markup=keyboard
        )
        set_user_state(user_id, OrderStates.products.state)
        await state.set_state(OrderStates.products)
    except Exception as e:
        await message.reply(f"❌ Error: {e}")


@router.message(StateFilter(OrderStates.products))
async def handle_product_input(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    language = get_user_language(user_id)
    selected_product_name = message.text

    try:
        product = get_product_by_name(selected_product_name, language)
        if not product:
            await message.reply(
                text=get_translation("product_not_found", language=language).replace("{name}", selected_product_name),
                parse_mode="HTML",
                reply_markup=generate_products_keyboard(language=language) 
            )
            return

        name_field = f"name_{language}"
        desc_field = "description"

        name = getattr(product, name_field, product.name_en or product.name_uz or product.name_ru)
        description = getattr(product, desc_field)
        price = f"{product.price} UZS"

        caption = (
            f"<b>{name}</b>\n\n"
            f"{description}\n\n"
            f"<b>{get_translation('price', language)}:</b> {price}"
        )

        keyboard = generate_product_keyboard(product.id, language)  

        if product.image_url:
            await bot.send_photo(
                chat_id=user_id,
                photo=FSInputFile(product.image_url),
                caption=caption,
                parse_mode="HTML",
                reply_markup=keyboard
            )
        else:
            await message.reply(
                text=caption,
                parse_mode="HTML",
                reply_markup=keyboard
            )

    except Exception as e:
        await message.reply(f"❌ Error: {e}")


@router.callback_query(F.data.startswith("add:"))
async def handle_add_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    language = get_user_language(user_id)

    product_id = int(callback.data.split(":")[1])
    product = get_product_by_id(product_id)

    basket_item = get_or_create_basket_item(user_id, product_id)
    save_basket_item(basket_item)

    quantity = basket_item.quantity
    price_total = product.price * quantity

    keyboard = generate_quantity_keyboard(product.id, quantity, language)

    caption = (
        f"<b>{getattr(product, f'name_{language}')}</b>\n\n"
        f"{product.description}\n\n"
        f"<b>{get_translation('price', language)}:</b> {price_total} UZS"
    )

    await callback.message.edit_caption(
        caption=caption,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(F.data.startswith("increase:"))
async def handle_increase_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    language = get_user_language(user_id)

    product_id = int(callback.data.split(":")[1])
    product = get_product_by_id(product_id)

    basket_item = get_or_create_basket_item(user_id, product_id)
    basket_item.quantity += 1
    save_basket_item(basket_item)

    price_total = product.price * basket_item.quantity

    keyboard = generate_quantity_only_keyboard(product_id, basket_item.quantity)

    caption = (
        f"<b>{getattr(product, f'name_{language}')}</b>\n\n"
        f"{product.description}\n\n"
        f"<b>{get_translation('price', language)}:</b> {price_total} UZS"
    )

    await callback.message.edit_caption(
        caption=caption,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(F.data.startswith("decrease:"))
async def handle_decrease_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    language = get_user_language(user_id)

    product_id = int(callback.data.split(":")[1])
    product = get_product_by_id(product_id)

    basket_item = get_or_create_basket_item(user_id, product_id)
    if basket_item.quantity > 1:
        basket_item.quantity -= 1
        save_basket_item(basket_item)

    price_total = product.price * basket_item.quantity

    keyboard = generate_counter_keyboard(product_id, basket_item.quantity)

    caption = (
        f"<b>{getattr(product, f'name_{language}')}</b>\n\n"
        f"{product.description}\n\n"
        f"<b>{get_translation('price', language)}:</b> {price_total} UZS"
    )

    await callback.message.edit_caption(
        caption=caption,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await callback.answer()


@router.message(StateFilter(UserStates.set_language, UserStates.menu, OrderStates.type, OrderStates.location, OrderStates.location_confirmation, OrderStates.items, OrderStates.subcategory, OrderStates.products))
async def handle_unrecognized_input(message: Message, state: FSMContext):
    
    current_state = await state.get_state()
    user_id = message.from_user.id
    language = get_user_language(user_id=user_id)
    user_location = get_user_location(user_id=user_id)
    state_responses = {
        UserStates.set_language: {
            "text": get_translation('start_text', language=language),
            "keyboard": language_keys()
        },
        UserStates.menu: {
            "text": get_translation('menu_message', language=language), 
            "keyboard": menu_keys(language=language)
        },
        OrderStates.type: {
            "text": get_translation("type", language=language),
            "keyboard": deliver_type_keys(language=language)
        },
        OrderStates.location: {
            "text": get_translation("location", language=language),
            "keyboard": location_keys(language=language, saved_location=user_location)
        },
        OrderStates.location_confirmation: {
            "text": get_translation(f"Your location: {user_location}", language=language),
            "keyboard": location_confirmation_keys(language=language)
        },
        OrderStates.items: {
            "text": get_translation("items_message", language=language),
            "keyboard": cate_keys(language=language)
        },
        OrderStates.subcategory: {
            "text": get_translation("subcategory_message", language=language),
            "keyboard": generate_subcategory_keyboard(language=language)
        },
        OrderStates.products: {
            "text": get_translation("products_message", language=language),
            "keyboard": generate_products_keyboard(language=language)
        }
    }
    response = state_responses.get(current_state, {
        "text": get_translation('menu_message', language),
        "keyboard": menu_keys(language=language)
    })
    await message.reply(
        response["text"],
        reply_markup=response["keyboard"],
        parse_mode='HTML'
    )


@router.message()
async def fallback_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_user_language(user_id=user_id)
    if user_exists(user_id=user_id) and language is not None:
        await message.reply(get_translation('menu_message', language=language), reply_markup=menu_keys(language=language), parse_mode="HTML")
        await state.set_state(UserStates.menu)
        set_user_state(user_id=user_id, state=UserStates.menu.state)
    else:
        await message.reply(get_translation('start_text', 'uz'), parse_mode='HTML', reply_markup=language_keys())
        await state.set_state(UserStates.start) 



