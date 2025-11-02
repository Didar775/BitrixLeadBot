# service/bitrix/webhook/handler.py
from fastapi import FastAPI, Form
from telegram.bot import bot, dp
from telegram.buttons import lead_action_keyboard
from telegram.constants import LEAD_INFO_TEMPLATE
from .base import Lead, get_lead_by_id

app = FastAPI()
USER_LEADS = {}


@app.post("/webhook/{chat_id}")
async def bitrix_webhook(
    chat_id: int,
    event: str = Form(...),
    event_handler_id: str = Form(...),
    ts: str = Form(...),
    data_fields_id: str = Form(..., alias="data[FIELDS][ID]")
):
    """
    Accept leads POSTed from Bitrix webhook and fetch full lead info.
    """
    lead_id = int(data_fields_id)

    # Fetch full lead info from Bitrix
    lead_data = await get_lead_by_id(lead_id)
    print(lead_data)
    if not lead_data:
        return {"status": "error", "message": f"Lead {lead_id} not found"}

    # Parse lead into your dataclass
    lead = Lead.from_bitrix(lead_data)


    # Save lead per chat
    USER_LEADS.setdefault(chat_id, []).append(lead)

    # Send Telegram message
    text = LEAD_INFO_TEMPLATE.format(
        id=lead.id,
        name=lead.name or "N/A",
        phone=lead.phone or "N/A",
        created_time=lead.date_create
    )

    try:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=lead_action_keyboard(lead.id))
    except Exception as e:
        return {"status": "error", "message": f"Telegram send_message failed: {e}"}

    return {"status": "ok", "lead_id": lead.id}
