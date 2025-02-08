"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#l6hub*@u(hw3+@p)csdro%l6z0eke32j8z29n-4wek7ki-h$f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'authorization.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "constance",
    'detailing',
    'authorization',
    'django_extensions',
    'rangefilter',
    'django_celery_beat'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TIME_ZONE = 'Almaty/Asia'
USE_TZ = True

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

CONSTANCE_CONFIG = {
    'STATUS_MESSAGE_TO_CLIENT': ("Уважаемый клиент, ваш статус обновлен: \n{new_status}\n\n"
                                 "Комментарий: \n{comment}\n\n"
                                 "Также вы можете посмотреть обновление на сайте: \n{client_link}",
                                 'сообщение клиенту, посвященное изменению статуса'),
    "FIRST_PUSH_MESSAGE_TO_CLIENT": ("Привет, спасибо что выбрали нас!",
                                     "сообщение клиенту, для первого оповещения о регистрации работы"),
    "FOLLOW_UP_MESSAGE": ("Привет! Уведомляю вас о том, что работа по вашей заявке начнется завтра.",
                          "сообщение за день до приема работы"),
    "FINAL_MESSAGE_TO_CLIENT": ("Привет! Уведомляю вас о том, что работа по вашей заявке полостью завершена.",
                                "сообщение после завершения работ"),

    'GREEN_API_INSTANCE_ID': ('__YOUR_ID__', 'id from your instance'),
    'GREEN_API_TOKEN': ('__YOUR_TOKEN__', 'TOKEN from your account'),
}

CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',  # Убедитесь, что адрес Redis правильный
        # 'LOCATION': 'redis://127.0.0.1:6379/0',  # Убедитесь, что адрес Redis правильный
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
# CONSTANCE_REDIS_CONNECTION = "redis://127.0.0.1:6379/0"  # Убедитесь, что используете правильный порт
CONSTANCE_REDIS_CONNECTION = "redis://redis:6379/0"  # Убедитесь, что используете правильный порт
CONSTANCE_DATABASE_CACHE_BACKEND = None

# CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# load_dotenv()


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'autodet'),
        'USER': os.getenv('DB_USER', 'autodet'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'autodet'),
        'HOST': os.getenv('DB_HOST', 'autodet-postgres-db'),
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'
