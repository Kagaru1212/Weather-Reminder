import requests
from django.core.mail import send_mail

from WeatherReminder import settings


def send(user_email, city_name):
    appid = '6dabbdf16a4a011fc0e41ae5cb097de4'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    res = requests.get(url.format(city_name)).json()

    city_info = {
        'city': city_name,
        'temp': res['main']['temp'],
        'humidity': res['main']['humidity'],
    }
    message_body = f"You've signed up for {city_name}. Temperature: {city_info['temp']}, Humidity: {city_info['humidity']}"

    send_mail(f"You've signed up for {city_name}", message_body, settings.EMAIL_HOST_USER, [user_email],
              fail_silently=False)


