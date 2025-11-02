from datetime import datetime

from urllib3.exceptions import ResponseError

from service.bitrix.structs.base import RESTLeads, Lead, TaskAdd, CreatedTask, TaskAddResult


class BaseResponse:
    data = None
    code = None

    def __init__(self, data: dict, code: int, headers: dict):
        self.data = data
        self.code = code
        self.headers = headers

    def parse_response(self):
        raise NotImplementedError

    def parse_errors(self):
        if "error" in self.data:
            raise ResponseError(self.data["error"])

    def parse(self):
        self.parse_errors()
        return self.parse_response()


class LeadListResponse(BaseResponse):
    def parse_errors(self):
        if self.code != 200:
            raise ResponseError(self.data)

    def parse_response(self) -> RESTLeads:
        result = self.data.get("result", [])
        leads = []
        for ld in result:
            leads.append(
                Lead(
                    id=int(ld["ID"]),
                    name=ld.get("NAME") or ld.get("TITLE") or "N/A",
                    status_id=ld.get("STATUS_ID"),
                    date_create=datetime.fromisoformat(ld.get("DATE_CREATE")),
                    assigned_by_id=int(ld.get("ASSIGNED_BY_ID") or 0),
                    opened=ld.get("OPENED", "Y") == "Y"
                )
            )
        return RESTLeads(leads=leads, total=len(leads))



class LeadUpdateResponse(BaseResponse):
    def parse_errors(self):
        if self.code != 200 or not self.data.get("result"):
            raise ResponseError(self.data)

    def parse_response(self):
        return self.data.get("result", False)


class TaskAddResponse(BaseResponse):
    def parse_errors(self):
        # According to docs: HTTP status 200 means success, result.task.id should exist
        if self.code != 200 or "result" not in self.data or "task" not in self.data["result"]:
            raise ResponseError(self.data)

    def parse_response(self) -> TaskAdd:
        # Parses JSON into TaskAddResponse data class
        # We'll assume you have some helper to convert dict → dataclass
        result_data = self.data["result"]
        task_data = result_data["task"]
        created_task = CreatedTask(
            id=task_data.get("id"),
            parentId=task_data.get("parentId"),
            title=task_data.get("title"),
            description=task_data.get("description"),
            deadline=task_data.get("deadline"),
            responsibleId=task_data.get("responsibleId"),
        )
        return TaskAdd(
            result=TaskAddResult(task=created_task),
            time=self.data.get("time", {})
        )