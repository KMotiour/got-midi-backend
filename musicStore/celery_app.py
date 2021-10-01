import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicStore.settings')
app = Celery('musicStore')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'add-every-2-hour':{
        'task':'youtube_api_update',
        'schedule':crontab(minute=0, hour='*/23')
    }
}



@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

