# Bitrix Lead Bot

This project integrates **Bitrix24 CRM** with a **Telegram bot**.  
It automatically checks for expired leads and sends notifications to the admin via Telegram.  
The admin can interact with leads (call, write, postpone) directly from Telegram, and actions are reflected in Bitrix24.

---

## Features

- Periodically checks for expired leads in Bitrix24.
- Sends lead information to the admin in Telegram.
- Inline buttons allow quick actions:
  - Call
  - Write
  - Postpone
- Actions performed in Telegram are synced back to Bitrix24.
- Configurable timezones for both local and Bitrix server.

---


### Demo Video

[![Demo Video](https://img.youtube.com/vi/vWcMu829Nvo/0.jpg)](https://youtu.be/vWcMu829Nvo)



## Requirements

- Python 3.13+
- Redis (local or remote)
- Virtualenv
- Bitrix24 account with API credentials
- Telegram Bot Token

---

## Environment Variables

Create a `.env` file in the **project root** and add the following variables:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ADMIN_CHAT_ID=your_telegram_chat_id

# Bitrix24 Webhook
# Create an incoming webhook in Bitrix24:
# Bitrix24 -> Applications -> Developer resources -> Other -> Incoming webhook
# Set permissions:
#   - Tasks (tasks)
#   - CRM (crm)
#   - REST (rest)
#   - Extended tasks (tasks_extended)
# Copy the generated URL and paste it here
BITRIX_WEBHOOK_URL=https://yourcompany.bitrix24.kz/rest/1/your_webhook/

# Redis (Celery broker & cache)
REDIS_URL=redis://localhost:6379/0

# Timezones
# Local timezone (optional, default: Asia/Almaty)
LOCAL_TIMEZONE=Asia/Almaty

# Bitrix server timezone (required!)
BITRIX_SERVER_TIMEZONE=Europe/Moscow

# Celery broker (optional, default: REDIS_URL)
CELERY_BROKER_URL=redis://localhost:6379/0
```



## Running the Bot

### 1. Start the bot and Redis (manual / on-demand mode)

```bash
chmod +x start.sh

./start.sh

```

Starts the Telegram bot.

Starts Redis (if not already running).

Use this mode if you want to check expired leads manually via a bot command.

The bot will only respond when you interact with it.


## Start Celery Worker & Beat (automatic / scheduled mode)
```bash
chmod +x start-celery.sh

./start-celery.sh

```


Runs the Celery worker and beat scheduler.
Periodically checks for expired leads based on the configured schedule.

Messages are sent automatically to the admin in Telegram.

Inline buttons allow immediate actions, synced back to Bitrix24.


### Celery Beat Schedule

By default, **Celery Beat** is scheduled to run the `check_expired_leads` task **every minute**:

```jsunicoderegexp
# Example from Celery schedule
'schedule': crontab(minute='*')

```
This fast schedule is useful during development and testing.

It allows you to see lead notifications almost immediately after they expire.

In production, you may want to adjust the interval (e.g., every hour) to reduce load:

### Example for hourly checks
```jsunicoderegexp
'schedule': crontab(minute=0, hour='*')
```


## Notes


Ensure Bitrix24 Webhook URL is valid.

Ensure timezones match your local and Bitrix server time.

Redis URL must be reachable by both bot and Celery.

Celery Beat can be adjusted to a real schedule (hourly, daily) after testing.
