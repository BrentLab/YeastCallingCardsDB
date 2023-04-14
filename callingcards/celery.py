import os
from celery import Celery
from configurations import importer
from dotenv import load_dotenv

load_dotenv() 
    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'callingcards.config')
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

importer.install()

app = Celery('callingcards')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['callingcards.callingcards'], related_name='tasks')
