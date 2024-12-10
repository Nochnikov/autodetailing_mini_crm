from django.db.models.signals import post_save
from django.dispatch import receiver
from detailing.models import Category
from .utils import send_whatsapp_message

@receiver(post_save, sender=Category)
def notify_status_change(sender, instance, **kwargs):
    client_phone = instance.client.phone_number
    new_status = instance.status.name_of_the_status
    message = f"Уважаемый клиент, ваш статус обновлен: {new_status}."
    send_whatsapp_message(client_phone, message)
