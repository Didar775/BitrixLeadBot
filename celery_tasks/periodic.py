from celery.schedules import crontab
from .celery import app
from settings.variables import LOCAL_TIMEZONE

app.conf.beat_schedule = {
    'check-expired-leads-every-hour': {
        'task': 'check_expired_leads',
        'schedule': crontab(minute='*'),
    },
}

app.conf.timezone = LOCAL_TIMEZONE
