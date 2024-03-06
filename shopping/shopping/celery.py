from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopping.settings')

celery_app = Celery('shopping')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
#time remain task in queue
# app.conf.result_expires=timedelta(days=30)
# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()



