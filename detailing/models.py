from django.core.exceptions import ValidationError
from django.db import models
import uuid

from django.utils import timezone

# Create your models here.

class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)

class Car(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    car_number = models.CharField(max_length=20, unique=True)
    car_mark = models.CharField(max_length=20)
    car_model = models.CharField(max_length=20)
    date_of_production = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    car_original_color = models.CharField(null=True, max_length=20, blank=True)

    def __str__(self):
        return f'{self.car_number}, {self.car_model}: {self.car_mark}.'

class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_of_the_status = models.CharField(max_length=20)
    description_of_the_status = models.TextField(null=True, blank=True)

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name_of_the_status}'

    class Meta:
        verbose_name_plural = 'Statuses'


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    job_status = models.CharField(max_length=50, choices=[
        ('awaiting_payment', 'Awaiting Prepayment'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='awaiting_payment')
    created_at = models.DateTimeField(default=timezone.now)

    def get_services(self):
        return Service.objects.filter(transitions__job=self).distinct()

    def __str__(self):
        services = ", ".join([service.name for service in self.get_services()])
        return f"Job {self.id} - Client: {self.client.first_name} {self.client.last_name}, Services: {services}"



class ServiceTransition(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='transitions')
    service = models.ForeignKey('Service', on_delete=models.CASCADE,  related_name='transitions')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='transitions')
    photo = models.ImageField(upload_to='transitions_photos/', blank=True, null=True)
    changed_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.service:
            self.service = self.job.service
        if self.pk:
            self.pk = None
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.service.name} - {self.status.name_of_the_status} ({self.changed_at})'

