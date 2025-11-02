# telegram/bot_setup.py
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from settings import variables

# Initialize Bot
bot = Bot(
    token=variables.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
    timeout=120
)

# Initialize Dispatcher (no bot argument!)
dp = Dispatcher()
