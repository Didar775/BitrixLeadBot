from datetime import datetime
from typing import Optional
from .rest_requests import LeadListRequest, LeadUpdateRequest, AddTaskRequest
from .rest_responses import RESTLeads
from settings import variables


class Client:
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or variables.BITRIX_WEBHOOK_URL

    async def get_leads(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None,
        status: str = "NEW",
        assigned_by_id: Optional[int] = None,
        start_index: int = 0,
    ) -> RESTLeads:
        """
        Получить список лидов по фильтрам.
        Время указывать в формате ISO 8601 (GMT+3).
        """

        params = {
            "FILTER[STATUS_ID]": status,
            "ORDER[DATE_CREATE]": "ASC",
            "SELECT[]": [
                "ID",
                "NAME",
                "STATUS_ID",
                "DATE_CREATE",
                "ASSIGNED_BY_ID",
                "OPENED",
            ],
            "START": start_index,
        }

        if start:
            params["FILTER[>DATE_CREATE]"] = start
        if end:
            params["FILTER[<DATE_CREATE]"] = end
        if assigned_by_id:
            params["FILTER[ASSIGNED_BY_ID]"] = assigned_by_id

        request = LeadListRequest(webhook_url=self.webhook_url, params=params)
        return await request.run()



    async def update_lead(self, lead_id: int, comment: str = None) -> dict:
        """
        Добавить комментарий к лиду.
        Использует метод crm.lead.comment.add
        """
        params = {
            "id": lead_id,
            "fields": {
                "COMMENTS": comment
            }
        }
        request = LeadUpdateRequest(webhook_url=self.webhook_url, params=params)
        return await request.run()

    async def add_task(self, lead_id: int, responsible_id: int, deadline: datetime, description: str) -> dict:
        """
        Создать задачу, связанную с лидом (tasks.task.add)
        """

        deadline_iso = deadline.strftime("%Y-%m-%dT%H:%M:%S%z")

        params = {
            "fields": {
                "TITLE": f"Follow up lead #{lead_id}",
                "RESPONSIBLE_ID": responsible_id,
                "DEADLINE": deadline_iso,
                "DESCRIPTION": description,
                "UF_CRM_TASK": [f"L_{lead_id}"],  # привязка к лиду
                "SE_PARAMETER": [
                    {"VALUE": "Y", "CODE": 3},
                    {"VALUE": "Y", "CODE": 2},
                ]
            }
        }

        request = AddTaskRequest(webhook_url=self.webhook_url, params=params)
        return await request.run()
