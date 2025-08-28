from django.apps import AppConfig


class WherehouseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.wherehouse'

    def ready(self):
        from . import admin
        from . import signals
        