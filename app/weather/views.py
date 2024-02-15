from rest_framework import generics
from django.shortcuts import render
from .models import Subscribing
from .serializers import WeatherSerializer


class WeatherApiView(generics.ListAPIView):
    queryset = Subscribing.objects.all()
    serializer_class = WeatherSerializer

