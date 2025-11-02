import aiohttp
from typing import Dict, Any
from .rest_responses import BaseResponse, LeadListResponse, LeadUpdateResponse, TaskAddResponse
from ..tools.http import RequestMethod


class BaseRequest:
    _path: str = "/"
    _method: str = RequestMethod.GET
    _response_class = BaseResponse

    def __init__(self, webhook_url: str, params: Dict[str, Any] = None):
        self.webhook_url = webhook_url.rstrip("/")
        self.params = params or {}

    async def _request(self):
        url = f"{self.webhook_url}{self._path}"
        async with aiohttp.ClientSession() as session:
            async with session.request(
                self._method,
                url,
                params=self.params if self._method == RequestMethod.GET else None,
                json=self.params if self._method == RequestMethod.POST else None,
                ssl=False
            ) as response:
                data = await response.json()
                return self._response_class(
                    data=data,
                    code=response.status,
                    headers=dict(response.headers)
                )

    async def run(self):
        """Return parsed response"""
        response = await self._request()
        return response.parse()


class LeadListRequest(BaseRequest):
    _path = "/crm.lead.list.json"
    _method = RequestMethod.POST
    _response_class = LeadListResponse



class LeadUpdateRequest(BaseRequest):
    """
    Обновляет лид и добавляет комментарий в поле COMMENTS.
    """
    _path = "/crm.lead.update.json"
    _method = RequestMethod.POST
    _response_class = LeadUpdateResponse


class AddTaskRequest(BaseRequest):
    """
    Добавляет задачу в Bitrix24 (crm.activity.add)
    """
    _path = "/tasks.task.add"
    _method = RequestMethod.POST
    _response_class = TaskAddResponse