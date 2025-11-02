import asyncio
from celery import shared_task
from service.bitrix_connector import BitrixConnector
from telegram.constants import LEAD_INFO_TEMPLATE
from telegram.bot import bot
from telegram.buttons import lead_action_keyboard
from settings.cache import save_leads_to_cache
from settings.variables import ADMIN_CHAT_ID

bitrix = BitrixConnector()


@shared_task(name='check_expired_leads')
def check_expired_leads_task():
    """
    Periodic task that checks for expired leads every hour.
    """
    try:
        # Use asyncio.run() to safely handle async code in Celery worker
        leads_data = asyncio.run(bitrix.get_expired_leads())
        leads = leads_data.leads

        if not leads:
            print("No expired leads found")
            return {"status": "success", "leads_count": 0}

        print(f"Found {len(leads)} expired leads")
        asyncio.run(send_lead_notifications(leads))

        return {
            "status": "success",
            "leads_count": len(leads),
            "lead_ids": [lead.id for lead in leads]
        }

    except Exception as e:
        print(f"Error in check_expired_leads_task: {e}")
        return {"status": "error", "message": str(e)}


async def send_lead_notifications(leads):
    """
    Sends lead information to the admin via Telegram
    and saves it to Redis cache.
    """
    user_id = ADMIN_CHAT_ID

    # ✅ Save to Redis cache
    await save_leads_to_cache(user_id, leads)

    for lead in leads:
        message = LEAD_INFO_TEMPLATE.format(
            id=lead.id,
            name=lead.name,
            phone=getattr(lead, "phone", "—"),
            created_time=lead.date_create.strftime("%Y-%m-%d %H:%M"),
        )

        try:
            await bot.send_message(
                chat_id=user_id,
                text=message,
                reply_markup=lead_action_keyboard(lead.id),
            )
        except Exception as e:
            print(f"Failed to send lead {lead.id}: {e}")


# Optional async helpers for commands
async def get_expired_leads_async():
    """
    Async function to get expired leads.
    Can be used by both command handler and Celery task.
    """
    try:
        leads_data = await bitrix.get_expired_leads()
        return leads_data.leads
    except Exception as e:
        print(f"Error fetching leads: {e}")
        raise


def format_lead_message(lead):
    """
    Format lead information for display.
    Shared function for both command and task.
    """
    return LEAD_INFO_TEMPLATE.format(
        id=lead.id,
        name=lead.name,
        phone=getattr(lead, "phone", "—"),
        created_time=lead.date_create.strftime("%Y-%m-%d %H:%M"),
    )
