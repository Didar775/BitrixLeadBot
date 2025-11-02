from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class Lead:
    id: int
    name: str
    status_id: str
    date_create: datetime
    assigned_by_id: Optional[int] = None
    opened: bool = True

@dataclass
class RESTLeads:
    leads: List[Lead] = field(default_factory=list)
    total: int = 0


@dataclass
class TaskField:
    TITLE: str
    RESPONSIBLE_ID: int
    DEADLINE: str
    DESCRIPTION: Optional[str] = None
    UF_CRM_TASK: Optional[List[str]] = field(default_factory=list)
    SE_PARAMETER: Optional[List[Dict[str, Any]]] = field(default_factory=list)

@dataclass
class CreatedTask:
    id: str
    parentId: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    responsibleId: Optional[str] = None

@dataclass
class TaskAddResult:
    task: CreatedTask

@dataclass
class TaskAdd:
    result: TaskAddResult
    time: Dict[str, Any]
