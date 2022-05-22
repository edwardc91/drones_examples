import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drones.settings")

app = Celery("drones")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()