import logging
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now
from .models import Job
from .utils import send_whatsapp_message
from constance import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ])

@shared_task
def checking_for_follow_up_task():
    try:
        jobs = Job.objects.filter(job_started__date=now() + timedelta(days=1))

        if jobs:
            for job in jobs:
                if job.created_at.date() == now():
                    continue
                send_whatsapp_message(job.client.phone_number, config.FOLLOW_UP_MESSAGE)
    except Exception as e:
        logging.error(e)



