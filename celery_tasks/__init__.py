from .celery import app
from .tasks import check_expired_leads_task
from . import periodic  # <-- ensure beat schedule is loaded

__all__ = ['app', 'check_expired_leads_task']
