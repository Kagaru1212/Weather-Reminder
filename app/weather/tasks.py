from celery import shared_task
from weather.service import send


@shared_task
def send_weather(user_email, city_name):
    send(user_email, city_name)

