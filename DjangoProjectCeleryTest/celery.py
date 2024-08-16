import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProjectCeleryTest.settings")

celery = Celery("celery")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()
