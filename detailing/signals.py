from django.dispatch import receiver
from django.utils import timezone

from .utils import send_whatsapp_message
from django.db.models.signals import post_save
from .models import ServiceTransition


@receiver(post_save, sender=ServiceTransition)
def notify_status_change(sender, instance, **kwargs):
    client_phone = instance.job.client.phone_number
    if instance.status:
        new_status = instance.status.name_of_the_status

        message = f"Уважаемый клиент, ваш статус обновлен: {new_status}."
        send_whatsapp_message(client_phone, message)
    else:
        pass

