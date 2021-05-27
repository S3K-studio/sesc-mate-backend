import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings


# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings.CELERY_DEBUG_MODE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sesc_mate.settings.production')

app = Celery('sesc_mate')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'check-schedule-every-15-min': {
        'task': 'notification_bot.tasks.check_schedule_for_changes',
        'schedule': crontab(minute=settings.CELERY_TIMER),
    },

    'announcements': {
        'task': 'api.tasks.announcements_polling',
        'schedule': crontab(minute='*/10'),
    },
}
