from django.db import models
import uuid
from django.utils import timezone

# Create your models here.

class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Номер телефона")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = 'Клиенты'
        verbose_name = 'Клиенты'

class Car(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    car_number = models.CharField(max_length=20, unique=True, verbose_name="Номер машины")
    car_mark = models.CharField(max_length=20, verbose_name="Марка машины")
    car_model = models.CharField(max_length=20, verbose_name="Модель машины")
    car_manufactured_date = models.PositiveIntegerField(null=True, blank=True, verbose_name="Дата производства")
    car_original_color = models.CharField(null=True, max_length=20, blank=True, verbose_name="Цвет машины")


    def __str__(self):
        return f'{self.car_number}, {self.car_mark}: {self.car_model} .'

    class Meta:
        verbose_name_plural = 'Машины'
        verbose_name = 'Машины'

class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name="Услуга")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name="Цена")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Усгули'
        verbose_name = 'Усгули'

class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_of_the_status = models.CharField(max_length=20, verbose_name="Статус")
    # description_of_the_status = models.TextField(null=True, blank=True, verbose_name="Описание")

    # service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")

    def __str__(self):
        return f'{self.name_of_the_status}'

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статусы'


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name="Клиент")
    car = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name="Машина")
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='jobs', verbose_name="Услуга")
    job_status = models.CharField(max_length=50, choices=[
        ('в_записи', 'В Записи'),
        ('в_процессе', 'В Процессе'),
        ('завершено', 'Завершено')
    ], default='в_записи', verbose_name="Статус работы")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Создано")
    job_started = models.DateTimeField(null=True, blank=True, verbose_name="Начато")
    pre_paid = models.PositiveIntegerField(null=True, blank=True, verbose_name="Предоплата")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # initial_status = Status.objects.filter(service=self.service).first()
            initial_status = Status.objects.all().first()

            if not initial_status:
                raise ValueError(f"No initial status found for service '{self.service.name}'. Please create a status.")

    def __str__(self):
        return f"Job {self.id} - {self.service.name}"

    class Meta:
        verbose_name_plural = 'Работы'
        verbose_name = 'Работы'


class ServiceTransition(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='transitions', verbose_name="Работа")
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='transitions', verbose_name="Статус")
    photo = models.ImageField(upload_to='transitions_photos/', blank=True, null=True, verbose_name="Фотография")
    changed_at = models.DateTimeField(default=timezone.now, verbose_name="Изменено в")
    comment = models.TextField(verbose_name="Комментарии")

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = ServiceTransition.objects.get(id=self.pk).status
            new_status = self.status

            if old_status != new_status:
                new_transition = ServiceTransition(
                    job=self.job,
                    status=new_status,
                    changed_at=timezone.now()
                )
                new_transition.save()
                return

        super(ServiceTransition, self).save(*args, **kwargs)

    def __str__(self):
        status_name = self.status.name_of_the_status if self.status else "No Status"
        return f"{self.job} - {status_name} ({self.changed_at})"

    class Meta:
        verbose_name_plural = 'Трек предоставленных работ'
        verbose_name = 'Трек предоставленных работ'


class WhatsAppNewsletter(models.Model):
    message = models.TextField(verbose_name="Сообщения для рассылки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return f"{self.message}: {self.created_at}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылка"