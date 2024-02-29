from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Subscribing
from .serializers import WeatherSerializer


class SubscribingApiViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the subscriptions of the current user
        return Subscribing.objects.filter(user=self.request.user)

