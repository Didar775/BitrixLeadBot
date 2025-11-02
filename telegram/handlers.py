from aiogram import Router, types, F, Bot
from aiogram.types import CallbackQuery
from telegram.buttons import lead_action_keyboard
from telegram.constants import (
    NO_LEADS_MSG, ERROR_MSG, LEAD_INFO_TEMPLATE,
    LEAD_UPDATED_MSG, TASK_CREATED_MSG,
    COMMENT_CALLED_MSG, COMMENT_WRITTEN_MSG,
    LEAD_NOT_FOUND_MSG, START_MSG, BLOCK_MSG,
)
from service.bitrix_connector import BitrixConnector
from settings.cache import get_lead_from_cache, save_leads_to_cache, delete_lead_from_cache
import asyncio

router = Router()
bitrix = BitrixConnector()


@router.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer(START_MSG)


@router.message(F.text == "/check_leads")
async def check_leads(message: types.Message):
    user_id = message.chat.id

    try:
        leads_data = await bitrix.get_expired_leads()
        leads = leads_data.leads

        if not leads:
            await message.answer(NO_LEADS_MSG)
            return

        # ✅ Save to Redis
        await save_leads_to_cache(user_id, leads)

        for lead in leads:
            text = LEAD_INFO_TEMPLATE.format(
                id=lead.id,
                name=lead.name,
                phone=getattr(lead, "phone", "—"),
                created_time=lead.date_create.strftime("%Y-%m-%d %H:%M"),
            )
            await message.answer(text, reply_markup=lead_action_keyboard(lead.id))

    except Exception as e:
        print(f"Error fetching leads: {e}")
        await message.answer(ERROR_MSG)


@router.callback_query(F.data.startswith(("called:", "wrote:", "postpone:")))
async def handle_lead_action(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id if callback.message else callback.from_user.id
    action, lead_id_str = callback.data.split(":")
    lead_id = int(lead_id_str)

    # ✅ Get lead from Redis
    lead = await get_lead_from_cache(user_id, lead_id)
    if not lead:
        await callback.answer(LEAD_NOT_FOUND_MSG, show_alert=True)
        return

    ACTIONS = {
        "called": {
            "comment": COMMENT_CALLED_MSG,
            "success": LEAD_UPDATED_MSG,
            "method": bitrix.write_comment_for_lead,
        },
        "wrote": {
            "comment": COMMENT_WRITTEN_MSG,
            "success": LEAD_UPDATED_MSG,
            "method": bitrix.write_comment_for_lead,
        },
        "postpone": {
            "method": bitrix.postpone_lead,
            "success": TASK_CREATED_MSG,
        },
    }

    try:
        action_data = ACTIONS.get(action)
        if not action_data:
            msg = await bot.send_message(chat_id, ERROR_MSG)
            await asyncio.sleep(3)
            await msg.delete()
            return

        if action in ("called", "wrote"):
            await action_data["method"](lead_id=lead["id"], comment=action_data["comment"])
        elif action == "postpone":
            await action_data["method"](lead_id=lead["id"], responsible_id=lead["assigned_by_id"])

        # ✅ Delete lead from cache and remove message after success
        await delete_lead_from_cache(user_id, lead_id)
        if callback.message:
            try:
                await callback.message.delete()
            except Exception:
                pass

        msg = await bot.send_message(chat_id, action_data["success"].format(lead_id=lead["id"]))
        await callback.answer()
        await asyncio.sleep(2)
        await msg.delete()

    except Exception as e:
        print(f"Error processing {action} for lead {lead_id}: {e}")
        error_msg = await bot.send_message(chat_id, ERROR_MSG)
        await callback.answer()
        await asyncio.sleep(2)
        await error_msg.delete()


@router.message()
async def block_text_messages(message: types.Message):
    if message.text not in ("/start", "/check_leads"):
        try:
            await message.delete()
        except Exception:
            pass

        warn = await message.answer(BLOCK_MSG)
        await asyncio.sleep(3)
        await warn.delete()
