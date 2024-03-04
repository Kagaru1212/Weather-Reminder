from django_celery_beat.models import PeriodicTask
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscribing
from .serializers import WeatherSerializer


class SubscribingApiViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the subscriptions of the current user
        return Subscribing.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Getting a periodic task by username and city name
        try:
            periodic_task = PeriodicTask.objects.get(name=f'{instance.user}_task_{instance.city_name}')
        except PeriodicTask.DoesNotExist:
            periodic_task = None

        # If a periodic task is found, delete it
        if periodic_task:
            periodic_task.delete()

        # Unsubscribe
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
