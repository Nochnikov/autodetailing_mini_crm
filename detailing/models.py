
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

class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_of_the_status = models.CharField(max_length=20, unique=True)
    description_of_the_status = models.TextField()

    def __str__(self):
        return f'{self.name_of_the_status}'

    class Meta:
        verbose_name_plural = 'Statuses'

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name_of_the_category = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)


    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'{self.name_of_the_category}, {self.pk}'


    class Meta:
        verbose_name_plural = 'Categories'










