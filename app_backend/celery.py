import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_backend.settings')

app = Celery('app_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# not sure what this does, but it is a requirment