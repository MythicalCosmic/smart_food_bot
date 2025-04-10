from aiogram import Router, Bot, F
from aiogram.types import Message, ContentType 
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from .states import UserStates, OrderStates
from config.settings import get_translation, get_button_text
from keyboards.keyboards import *
from utils.utils import *
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


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

@router.message(lambda message: message.text == get_button_text('hand_deliver', get_user_language(message.from_user.id)), StateFilter(OrderStates.type))
async def order_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=OrderStates.items.state)
        await message.reply(get_translation("items", language=language), parse_mode="HTML")
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
        print(f"lat: {latitude} long {longitude}")

        set_user_state(user_id=user_id, state=OrderStates.location_confirmation.state)
        add_user_location(user_id=user_id, latitude=latitude, longitude=longitude)
        geolocator = Nominatim(user_agent="my_telegram_bot")
        try:
            location = geolocator.reverse((latitude, longitude), timeout=10)
            address = location.address if location else "Unknown location"
        except GeocoderTimedOut:
            address = "Address lookup timed out"
        await message.reply(
            f"📍 <b>Your location:</b>\n{address}\n\n"
            f"✅ If it's correct, press Confirm.\n"
            f"❌ If not, send location again.",
            parse_mode="HTML", reply_markup=location_confirmation_keys(language=language)
        )
        await state.set_state(OrderStates.location_confirmation)
    except Exception as e:
        await message.reply(f"⚠️ Error occurred: {e}")


@router.message(lambda message: any(word in message.text.lower() for word in ["andijon", "o'zbekiston", "marhamat"]), StateFilter(OrderStates.location))
async def handle_items(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=OrderStates.items.state)
        await message.reply("Welcome to Items section")
        await state.set_state(OrderStates.items)
    except Exception as e:
        await message.reply(f"Error occured: {e}")



@router.message(StateFilter(UserStates.menu))
async def menu_handler(message: Message, state: FSMContext, bot: Bot):
    
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        await message.reply(get_translation('menu_message', language=language), reply_markup=menu_keys(language=language), parse_mode="HTML")
        set_user_state(user_id=user_id, state=UserStates.menu.state)
    except Exception as e:
        await message.reply(f"Error occured: {e}")

@router.message(lambda message: message.text == get_button_text("back", get_user_language(message.from_user.id)), StateFilter(OrderStates.type, OrderStates.location, OrderStates.location_confirmation))
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
        state_actions = {
            OrderStates.type.state: go_to_main_menu,
            OrderStates.location.state: go_to_order_type,
            OrderStates.location_confirmation: go_to_location
        }

        action = state_actions.get(current_state)
        if action:
            await action()
        else:
            await message.answer("Unknown state. Please try again.")

    except Exception as e:
        await message.reply(f"Error occurred: {e}")

@router.message(StateFilter(UserStates.set_language, UserStates.menu, OrderStates.type, OrderStates.location, OrderStates.location_confirmation))
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