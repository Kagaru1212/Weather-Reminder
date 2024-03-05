from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


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


    @extend_schema(
        description="Delete a specific subscription by ID",
        parameters=[OpenApiParameter(name='id', description='Subscription id', type=OpenApiTypes.INT,
                                     location=OpenApiParameter.PATH)],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        description="A list of all your subscriptions",
        responses={200: WeatherSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Create a new subscription.",
        request=WeatherSerializer,
        responses={201: WeatherSerializer()},
        parameters=[
            OpenApiParameter(name='city_name', description='The name of the city for the subscription.',
                             type=OpenApiTypes.STR),
            OpenApiParameter(name='notification',
                             description='The frequency of data sending (every 3, 6, or 12 hours).',
                             type=OpenApiTypes.INT),
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Retrieve a specific subscription by ID",
        responses={200: WeatherSerializer()},
        parameters=[OpenApiParameter(name='id', description='Subscription id', type=OpenApiTypes.INT,
                                     location=OpenApiParameter.PATH)],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Update a specific subscription by ID",
        request=WeatherSerializer,
        responses={200: WeatherSerializer()},
        parameters=[
            OpenApiParameter(name='id', description='Subscription id', required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH),
            OpenApiParameter(name='notification',
                             description='The frequency of data sending (every 3, 6, or 12 hours).',
                             type=OpenApiTypes.INT),
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description="Partial update of a specific subscription by ID",
        request=WeatherSerializer,
        responses={200: WeatherSerializer()},
        parameters=[
            OpenApiParameter(name='id', description='Subscription id', type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH),
            OpenApiParameter(name='notification',
                             description='The frequency of data sending (every 3, 6, or 12 hours).',
                             type=OpenApiTypes.INT),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
