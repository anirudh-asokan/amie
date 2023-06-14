import os
from celery import Celery
from django.conf import settings

app = Celery('amie')
app.config_from_object('django.conf:settings')

# Use this line below if your tasks are spread across several apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)