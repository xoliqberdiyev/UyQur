from django.conf import settings

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = settings.TIME_ZONE
CELERY_ENABLED = True

