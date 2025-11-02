import pytz
from datetime import datetime, timedelta
from service.bitrix.client import Client
from service.bitrix.structs.base import RESTLeads
from settings.variables import BITRIX_WEBHOOK_URL, LOCAL_TIMEZONE, BITRIX_SERVER_TIMEZONE


class BitrixConnector:
    def __init__(self, webhook_url: str = None, local_tz: str = None, server_tz: str = None):
        self.webhook_url = webhook_url or BITRIX_WEBHOOK_URL
        self.client = Client(webhook_url=self.webhook_url)
        self.local_tz = pytz.timezone(local_tz or LOCAL_TIMEZONE)
        self.server_tz = pytz.timezone(server_tz or BITRIX_SERVER_TIMEZONE)

    async def get_expired_leads(self, hours: int = 2) -> RESTLeads:
        """
        Get leads with status NEW that were created more than `hours` hours ago.
        """

        now_local = datetime.now(self.local_tz)
        cutoff_local = now_local - timedelta(hours=hours)

        # Преобразуем локальное время (например, Asia/Almaty, GMT+5) в серверное (Europe/Moscow, GMT+3)
        cutoff_server = cutoff_local.astimezone(self.server_tz)

        print(
            f"[LOCAL] Now: {now_local} | Cutoff: {cutoff_local}\n"
            f"[SERVER] Cutoff: {cutoff_server}"
        )

        # Берём всё, что создано раньше cutoff_server
        return await self.client.get_leads(
            end=cutoff_server.strftime("%Y-%m-%dT%H:%M:%S%z"),
            status="NEW",
        )


    async def write_comment_for_lead(self, lead_id: int, comment: str):
        return await self.client.update_lead(
            lead_id=lead_id,
            comment=comment
        )


    async def postpone_lead(self, lead_id: int,
                            responsible_id: int,
                            hours: int = 2,
                            description: str = None,):
        """
        Создать задачу в Bitrix для лида с дедлайном через 2 часа.
        """
        server_tz = pytz.timezone("Europe/Moscow")  # GMT+3
        deadline = datetime.now(server_tz) + timedelta(hours=hours)

        description = description or f"Postpone lead #{lead_id} for {hours} hours"

        return await self.client.add_task(
            lead_id=lead_id,
            responsible_id=responsible_id,
            deadline=deadline,
            description=description,
        )
