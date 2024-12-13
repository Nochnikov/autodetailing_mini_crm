from django.core.exceptions import ValidationError
from django.db import models
import uuid

from django.utils import timezone

# Create your models here.

class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

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
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='jobs')
    job_status = models.CharField(max_length=50, choices=[
        ('awaiting_payment', 'Awaiting Prepayment'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='awaiting_payment')
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Проверяем, создаётся ли новый объект
        super().save(*args, **kwargs)

        if is_new:
            # Пытаемся получить начальный статус
            initial_status = Status.objects.filter(service=self.service).first()

            if not initial_status:
                raise ValueError(f"No initial status found for service '{self.service.name}'. Please create a status.")

    def __str__(self):
        return f"Job {self.id} - {self.service.name}"


class ServiceTransition(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='transitions')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='transitions')
    photo = models.ImageField(upload_to='transitions_photos/', blank=True, null=True)
    changed_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Проверяем, если это обновление (не создание новой записи)
        if self.pk:
            # Получаем старый статус из базы данных перед изменением
            old_status = ServiceTransition.objects.get(id=self.pk).status
            new_status = self.status

            # Если статус изменился, создаем новый объект в ServiceTransition
            if old_status != new_status:
                # Создаем новый переход с новым статусом
                new_transition = ServiceTransition(
                    job=self.job,
                    status=new_status,
                    changed_at=timezone.now()  # Записываем текущую дату и время изменения
                )
                new_transition.save()  # Сохраняем новый переход
                return  # Выходим из текущего сохранения

        # Если статус не изменился, продолжаем стандартное сохранение
        super(ServiceTransition, self).save(*args, **kwargs)
    def __str__(self):
        status_name = self.status.name_of_the_status if self.status else "No Status"
        return f"{self.job} - {status_name} ({self.changed_at})"
