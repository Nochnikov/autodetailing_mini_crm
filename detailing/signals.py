from django.dispatch import receiver
from constance.signals import config_updated
from constance import config
from .utils import send_whatsapp_message
from django.db.models.signals import post_save
from .models import ServiceTransition


@receiver(config_updated)
def constance_update(sender, key, old_value, new_value, **kwargs):
    print(sender, key, old_value, new_value)


@receiver(post_save, sender=ServiceTransition)
def notify_status_change(sender, instance, **kwargs):
    client_phone = instance.job.client.phone_number
    if instance.status:
        new_status = instance.status.name_of_the_status
        message = config.MESSAGE + new_status
        send_whatsapp_message(client_phone, message)
    else:
        pass
