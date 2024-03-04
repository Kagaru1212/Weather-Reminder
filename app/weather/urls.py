from rest_framework import routers
from .views import SubscribingApiViewSet

router = routers.SimpleRouter()
router.register(r'subscriptions', SubscribingApiViewSet, basename='subscriptions')

urlpatterns = []
