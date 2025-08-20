from django.apps import AppConfig


class CounterpatyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.counterparty'

    def ready(self):
        from . import admin 
        