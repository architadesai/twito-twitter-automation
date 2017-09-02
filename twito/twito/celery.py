from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

class Config:
	#Configuration for celery tasks::

	BROKER_URL = 'amqp://guest:guest@localhost:5672//'
	CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost:5672//'
	CELERY_ACCEPT_CONTENT = ['application/json']
	CELERY_TASK_SERIALIZER = 'json'
	CELERY_RESULT_SERIALIZER = 'json'
	CELERY_TIMEZONE = 'Asia/Calcutta'



#Set default configuration module name
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

#Create instance of Celery
app = Celery('twito')

app.config_from_object(Config)

#To find tasks.py file from apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
