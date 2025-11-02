from celery import Celery
from settings.variables import CELERY_BROKER_URL, LOCAL_TIMEZONE

app = Celery(
    'bitrix_lead_bot',
    broker=CELERY_BROKER_URL,
    include=['celery_tasks.tasks']
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone=LOCAL_TIMEZONE,
    enable_utc=False,
    task_track_started=True,
)

if __name__ == '__main__':
    app.start()
