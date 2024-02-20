from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('users/register/', views.UserRegistrationView.as_view(), name='register'),
]
