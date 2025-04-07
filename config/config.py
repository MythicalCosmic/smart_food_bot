from aiogram import Bot, Dispatcher
import logging
from config.settings import BOT_TOKEN, ADMIN_ID
from handlers.handlers import router
from middlewares.middlewares import UserRegistrationMiddleware



if not BOT_TOKEN:
    logging.critical("BOT_TOKEN is missing! Please check your .env file.")
    exit(1)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.message.middleware(UserRegistrationMiddleware())
dp.include_router(router)


try:
    ADMIN_ID = int(ADMIN_ID) if ADMIN_ID else None
except ValueError:
    logging.warning("ADMIN_ID is not a valid integer. Ignoring admin functionality.")

logging.info("Bot and Dispatcher initialized successfully.")
