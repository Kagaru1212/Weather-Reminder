import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import generics
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .models import Subscribing
from .serializers import WeatherSerializer


class WeatherApiView(generics.ListCreateAPIView):
    """
    This class is responsible for creating and reading subscription data.
    Roughly speaking the implementation of methods (GET, POST).
    Also, the GET of this class returns all existing subscriptions.
    """
    queryset = Subscribing.objects.all()
    serializer_class = WeatherSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save()


class WeatherApiUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    This class is responsible for reading, modifying and deleting subscriptions.
    Implementation of methods (GET, PUT, DELETE).
    Only in this class the GET method is used to output one specific subscription, not all subscriptions.
    """
    queryset = Subscribing.objects.all()
    serializer_class = WeatherSerializer

    def perform_update(self, serializer):
        serializer.save()


def weather(request, pk):
    appid = '6dabbdf16a4a011fc0e41ae5cb097de4'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    # Получаем информацию о текущем пользователе из запроса
    user = request.user

    # Проверяем, есть ли у пользователя подписка
    try:
        subscribing = Subscribing.objects.get(user=user, pk=pk)
        city = subscribing.city_name  # Получаем имя города из подписки
        res = requests.get(url.format(city)).json()

        city_info = {
            'city': city,
            'temp': res['main']['temp'],
            'humidity': res['main']['humidity'],
        }

        return JsonResponse(city_info)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User has no subscription with specified pk'}, status=400)
