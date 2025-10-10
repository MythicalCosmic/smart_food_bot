import os
import logging
from dotenv import load_dotenv
import yaml

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


PAYME_TOKEN = os.getenv("PAYME_TOKEN")
CLICK_TOKEN = os.getenv("CLICK_TOKEN")


WEBHOOK = os.getenv("WEBHOOK", "False").lower() == "true"
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")


DEBUG = os.getenv("DEBUG", "True").lower() == "true"
DEBUG_LEVEL = os.getenv("DEBUG_LEVEL", "info").upper()


LOG_DIR = "requests"
LOG_FILE = f"{LOG_DIR}/request.log"


os.makedirs(LOG_DIR, exist_ok=True)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
LANGUAGES_FILE = os.path.join(BASE_DIR, "languages", "uz.yaml")

with open(LANGUAGES_FILE, "r", encoding="utf-8") as file:
    LANGUAGES = yaml.safe_load(file)

    

def get_translation(key: str, language: str) -> str:
    keys = key.split(".")  
    data = LANGUAGES.get(language, LANGUAGES["uz"])
    for k in keys:
        data = data.get(k, {})
    if isinstance(data, str):
        return data
    return key


def get_button_text(button_key: str, language: str) -> str:
    return LANGUAGES.get(language, LANGUAGES["uz"]).get("buttons", {}).get(button_key, button_key)


logging.basicConfig(
    level=getattr(logging, DEBUG_LEVEL, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ],
)
logging.info("Configuration loaded successfully.")
