from django.apps import AppConfig


class DetailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detailing'

    def ready(self):
        import detailing.signals
