import requests
from django.core.mail import send_mail


def send(user_email, city_name):
    appid = '6dabbdf16a4a011fc0e41ae5cb097de4'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    res = requests.get(url.format(city_name)).json()

    city_info = {
        'city': city_name,
        'temp': res['main']['temp'],
        'humidity': res['main']['humidity'],
    }
    send_mail(f"You've signed up for {city_name}", city_info, 'djangositetest1@gmail.com', [user_email], fail_silently=False)
