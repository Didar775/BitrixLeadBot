# ───────────────────────────────
# System messages
# ───────────────────────────────
START_MSG = (
    "👋 Hello! I’m your assistant bot for Bitrix24.\n\n"
    "Use the command /check_leads to get a list of leads "
    "that were created more than 2 hours ago."
)

CONNECTED_MSG = "✅ Connection to Bitrix established successfully!"
NO_LEADS_MSG = "📭 No new leads older than 2 hours."
ERROR_MSG = "⚠️ Something went wrong. Please try again later."
LEAD_NOT_FOUND_MSG = "⚠️ Lead not found in cache. Please refresh leads."
BLOCK_MSG = '❗ Please use bot commands or buttons only.'

# ───────────────────────────────
# Actions / Buttons
# ───────────────────────────────
BTN_CALLED = "✅ Called"
BTN_WRITTEN = "💬 Wrote"
BTN_POSTPONE = "⏳ Postpone for 2 hours"

# ───────────────────────────────
# Templates
# ───────────────────────────────
LEAD_INFO_TEMPLATE = (
    "📋 <b>Lead #{id}</b>\n"
    "👤 {name}\n"
    "📞 {phone}\n"
    "🕒 Created: {created_time}"
)

# ───────────────────────────────
# Action confirmations
# ───────────────────────────────
COMMENT_CALLED_MSG = "✅ Client called"
COMMENT_WRITTEN_MSG = " Message sent to client"

LEAD_UPDATED_MSG = "✅ Comment added to Bitrix for lead #{lead_id}."
TASK_CREATED_MSG = "🕓 Task created in Bitrix for lead #{lead_id}, deadline +2h."
