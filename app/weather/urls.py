from django.urls import path
from . import views

urlpatterns = [
    path('subscriptions/', views.WeatherApiView.as_view()),
    path('subscriptions/<int:pk>/', views.WeatherApiUpdate.as_view()),
    path('subscriptions/me/', views.SubscribingUserApiView.as_view()),
    path('subscriptions/<int:pk>/me/', views.SubscribingUserApiUpdate.as_view()),
]
