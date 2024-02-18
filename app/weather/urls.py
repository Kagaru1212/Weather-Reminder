from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/subscribing/', views.WeatherApiView.as_view()),
    path('api/v1/subscribing/<int:pk>/', views.WeatherApiUpdate.as_view()),
    path('api/v1/subscribing/<int:pk>/weather/', views.weather),
]
