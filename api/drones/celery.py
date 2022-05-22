import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drones.settings")

app = Celery("drones")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check_drone_battery_task": {
        "task": "base.tasks.check_drone_battery_task",
        "schedule": crontab(minute="*"),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')