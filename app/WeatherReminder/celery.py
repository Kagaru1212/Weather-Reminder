import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeatherReminder.settings')

app = Celery('WeatherReminder')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'send-weather-every-3-minutes': {
        'task': 'weather.tasks.send_weather',
        'schedule': 180,
    },
    'send-weather-every-6-minutes': {
        'task': 'weather.tasks.send_weather',
        'schedule': 360,
    },
    'send-weather-every-12-minutes': {
        'task': 'weather.tasks.send_weather',
        'schedule': 720,
    },
}
