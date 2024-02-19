from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/subscriptions', views.WeatherApiView.as_view()),
    path('api/v1/subscriptions/<int:pk>/', views.WeatherApiUpdate.as_view()),
]
