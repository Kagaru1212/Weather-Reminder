import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django_celery_beat.models import PeriodicTask
from rest_framework import generics, status
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Получаем периодическую задачу по имени пользователя и названию города
        try:
            periodic_task = PeriodicTask.objects.get(name=f'{instance.user}_task_{instance.city_name}')
        except PeriodicTask.DoesNotExist:
            periodic_task = None

        # Если найдена периодическая задача, удаляем ее
        if periodic_task:
            periodic_task.delete()

        # Удаляем подписку
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



