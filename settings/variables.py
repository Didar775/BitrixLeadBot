import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

BITRIX_WEBHOOK_URL = os.getenv("BITRIX_WEBHOOK_URL")

LOCAL_TIMEZONE = os.getenv("LOCAL_TIMEZONE", 'Asia/Almaty')
BITRIX_SERVER_TIMEZONE = os.getenv("BITRIX_SERVER_TIMEZONE", 'Europe/Moscow')

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

REDIS_URL=os.getenv("REDIS_URL", "redis://localhost:6379/0")