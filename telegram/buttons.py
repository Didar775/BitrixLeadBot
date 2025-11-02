from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import BTN_CALLED, BTN_WRITTEN, BTN_POSTPONE

def lead_action_keyboard(lead_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=BTN_CALLED, callback_data=f"called:{lead_id}"),
                InlineKeyboardButton(text=BTN_WRITTEN, callback_data=f"wrote:{lead_id}"),
            ],
            [
                InlineKeyboardButton(text=BTN_POSTPONE, callback_data=f"postpone:{lead_id}")
            ]
        ]
    )