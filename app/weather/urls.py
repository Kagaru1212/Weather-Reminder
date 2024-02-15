from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/weather', views.WeatherApiView.as_view()),
]
