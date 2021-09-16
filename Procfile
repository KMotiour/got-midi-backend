web: gunicorn musicStore.wsgi --log-file -
worker: celery -A musicStore worker -l info -B
