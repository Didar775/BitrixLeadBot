# settings/cache.py
import json
import redis.asyncio as redis  # ✅ modern async redis
from .variables import REDIS_URL

import json
from datetime import datetime

def lead_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj.__dict__

async def get_redis():
    return redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def save_leads_to_cache(user_id: int, leads: list):
    r = await get_redis()

    leads_data = {str(lead.id): json.dumps(lead, default=lead_encoder) for lead in leads}

    await r.hset(f"leads:{user_id}", mapping=leads_data)

async def get_lead_from_cache(user_id: int, lead_id: int):
    r = await get_redis()
    lead_data = await r.hget(f"leads:{user_id}", str(lead_id))
    return json.loads(lead_data) if lead_data else None

async def delete_lead_from_cache(user_id: int, lead_id: int):
    r = await get_redis()
    await r.hdel(f"leads:{user_id}", str(lead_id))