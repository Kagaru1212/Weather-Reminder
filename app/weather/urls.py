from rest_framework import routers
from .views import SubscribingApiViewSet

router = routers.SimpleRouter()
router.register(r'subscriptions', SubscribingApiViewSet, basename='subscriptions')

urlpatterns = [
    path('api/v1/subscribing/', views.WeatherApiView.as_view()),
    path('api/v1/subscribing/<int:pk>/', views.WeatherApiUpdate.as_view()),
]
