from celery import shared_task
from musicStore.celery_app import app
from .models import YoutubeApi


@shared_task
def send_instant_mail(id):
    print('helo')

@app.task(name='youtube_api_update')
def youtube_api_update():
    try:
        YoutubeApi.objects.all().update(count=30)
        return True
    except Exception as e:
        print(e)