from django.dispatch import receiver
from constance.signals import config_updated
from constance import config
from django.http import Http404

from .utils import send_whatsapp_message
from django.db.models.signals import post_save
from .models import ServiceTransition, Job, WhatsAppNewsletter, Client


@receiver(config_updated)
def constance_update(sender, key, old_value, new_value, **kwargs):
    print(sender, key, old_value, new_value)


@receiver(post_save, sender=ServiceTransition)
def notify_status_change(sender, instance, **kwargs):
    client_phone = instance.job.client.phone_number
    if instance.status:
        new_status = instance.status.name_of_the_status
        message = (config.STATUS_MESSAGE_TO_CLIENT + "\n\n" + new_status + "\n\nОписание:" +
                   "\n\n" + f"{instance.status.description_of_the_status}" + "\n\n\n"
                   # + f"http://127.0.0.1:8000/user_side/service/{instance.job.id}/")
                   + f"http://194.32.141.192:8000/user_side/service/{instance.job.id}/")
        send_whatsapp_message(client_phone, message)
    else:
        pass


@receiver(post_save, sender=Job)
def hello_message(sender, instance, created=None, **kwargs):
    if created:
        client_phone = instance.client.phone_number
        if client_phone:
            message = config.FIRST_PUSH_MESSAGE_TO_CLIENT
            send_whatsapp_message(client_phone, message)
        else:
            raise Http404("Client not found")

@receiver(post_save, sender=WhatsAppNewsletter)
def newsletter_message(sender, instance, created=None, **kwargs):
    if created:
        client = Client.objects.all()
        message = instance.message
        for i in range(len(client)):
            phone_number = client[i].phone_number
            send_whatsapp_message(phone_number, message)


