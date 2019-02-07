import os
import django
import datetime
from celery import Celery
from django.conf import settings
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

app = Celery('Main', broker=settings.BROKER_URL, include=['core.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
queue_name = 'celery'
app.conf.task_queues = [Queue(queue_name, Exchange(queue_name), routing_key=queue_name)]

app.conf.broker_transport_options = {'visibility_timeout': 7200}

app.conf.beat_schedule = {
    'clean_log': {
        'task': 'CleanLog',
        'schedule': datetime.timedelta(days=1),
    },
    'update_holidays': {
        'task': 'UpdateHolidays',
        'schedule': datetime.timedelta(days=7),
    }
}