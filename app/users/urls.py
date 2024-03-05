from django.urls import path
from . import views
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView

app_name = 'users'

urlpatterns = [
    path('users/register/', views.UserRegistrationView.as_view(), name='register'),
    path('users/me/', views.UserUpdate.as_view(), name='update_user'),
    path('users/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('users/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
]
