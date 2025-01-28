from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from authorization.managers import UserManager
class User(AbstractBaseUser, PermissionsMixin):

    MALE, FEMALE = 1, 2
    GENDER_CHOICES = ((MALE, 'male'),
                      (FEMALE, 'female'))

    username = models.CharField(max_length=100, unique=True, verbose_name="Имя пользовтеля")
    email = models.EmailField(unique=False, verbose_name="Электронная почта")
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    gender = models.IntegerField(choices=GENDER_CHOICES, default=MALE, verbose_name="Пол")


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.username}:{self.password}, {self.is_superuser}'


    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'

