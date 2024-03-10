# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import sys
sys.path.append('/Users/mac/Desktop/handleregisterApi/core')

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# create a Celery instance and configure it using the settings from Django.
app = Celery('core')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
