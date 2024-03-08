from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer, UserUpdateSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        description="Please register.",
        request=UserSerializer,
        responses={201: UserSerializer()},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PUT' or 'PATCH':
            return UserUpdateSerializer

        return UserSerializer

    @extend_schema(
        description="Your data.",
        responses={200: UserSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Update your data (username or password)",
        request=UserUpdateSerializer,
        responses={200: UserSerializer()},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        description="Update your data (username or password)",
        request=UserUpdateSerializer,
        responses={200: UserSerializer()},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


@extend_schema(
    description="Generate an access and refresh JSON web token pair by providing user credentials. Both tokens will work for one day",
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    description="Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.",
    parameters=[
        OpenApiParameter(name='refresh',
                         description='Enter a you refresh token.', type=OpenApiTypes.STR),
    ],
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(
    description="Takes a token and indicates if it is valid. This view provides no information about a token's fitness for a particular use.",
    parameters=[
        OpenApiParameter(name='token',
                         description='Enter a token.', type=OpenApiTypes.STR),
    ],
)
class CustomTokenVerifyView(TokenVerifyView):
    pass