import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

celery_app = Celery('mysite')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'checking_for_follow_up_task': {
        'task': 'detailing.tasks.checking_for_follow_up_task',
        'schedule': crontab(hour='9', minute='0'),
        # 'schedule': crontab(minute='*'),
    },
}


