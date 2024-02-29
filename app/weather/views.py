import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import generics
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

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

