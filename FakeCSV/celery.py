import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FakeCSV.settings')
app = Celery('alarms')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'search_for_new_dataset': {
        'task': 'schemas.tasks.search_for_new_dataset',
        'schedule': 60.0
    },

}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
