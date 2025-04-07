from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from .states import UserStates
from config.settings import get_translation
from keyboards.keyboards import *
from utils.utils import *


router = Router()


@router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        if user_exists(user_id=user_id) and language is not None:
            await message.reply(get_translation('menu_message', language=language), reply_markup=menu_keys())
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
            "Ingliz tili": "en",
            "Ozbek Tili": "uz",
            "Русский язык": "ru" 
        }
        language = language_map.get(message.text, "ru")
        set_user_state(user_id=user_id, state=UserStates.set_language.state)
        set_language_user(user_id=user_id, language=language)
        user_language = get_user_language(user_id=user_id)
        await message.reply(get_translation('menu_message', user_language), reply_markup=menu_keys(), parse_mode="HTML")
        set_user_state(user_id=user_id, state=UserStates.menu.state)
        await state.set_state(UserStates.menu)
    except Exception as e:
        await message.reply(f'Error occurred: {e}')

@router.message(StateFilter(UserStates.menu))
async def menu_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        print(language)
        await message.reply(get_translation('menu_message', language=language), reply_markup=menu_keys(), parse_mode="HTML")
        await state.clear()
    except Exception as e:
        await message.reply(f"Error occured: {e}")


@router.message(StateFilter(UserStates.set_language, UserStates.menu))
async def handle_unrecognized_input(message: Message, state: FSMContext):
    current_state = await state.get_state()
    user_id = message.from_user.id
    language = get_user_language(user_id=user_id)
    state_responses = {
        UserStates.set_language: {
            "text": get_translation('start_text', language),
            "keyboard": language_keys()
        },
        UserStates.menu: {
            "text": get_translation('menu_message', language), 
            "keyboard": menu_keys()
        },
    }
    response = state_responses.get(current_state, {
        "text": get_translation('menu_message', language),
        "keyboard": menu_keys()
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
        await message.reply(get_translation('menu_message', language=language), reply_markup=menu_keys(), parse_mode="HTML")
        await state.set_state(UserStates.menu)
        set_user_state(user_id=user_id, state=UserStates.menu.state)
    else:
        await message.reply(get_translation('start_text', 'uz'), parse_mode='HTML', reply_markup=language_keys())
        await state.set_state(UserStates.start) 