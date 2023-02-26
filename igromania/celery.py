import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "igromania.settings")
app = Celery("igromania")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: ['applications.news'])