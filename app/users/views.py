from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer
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
        parameters=[
            OpenApiParameter(name='Username', description='Enter a username.',
                             type=OpenApiTypes.STR),
            OpenApiParameter(name='Email',
                             description='Enter a email.',
                             type=OpenApiTypes.STR),
            OpenApiParameter(name='Password',
                             description='Enter a password.',
                             type=OpenApiTypes.STR),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        description="Your data.",
        responses={200: UserSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Update your data (username or password)",
        request=UserSerializer,
        responses={200: UserSerializer()},
        parameters=[
            OpenApiParameter(name='username',
                             description='Enter a new username.', type=OpenApiTypes.STR),
            OpenApiParameter(name='password',
                             description='Enter a new password.', type=OpenApiTypes.STR),
        ],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        description="Update your data (username or password)",
        request=UserSerializer,
        responses={200: UserSerializer()},
        parameters=[
            OpenApiParameter(name='username',
                             description='Enter a new username.', type=OpenApiTypes.STR),
            OpenApiParameter(name='password',
                             description='Enter a new password.', type=OpenApiTypes.STR),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


@extend_schema(
    description="Generate an access and refresh JSON web token pair by providing user credentials. Both tokens will work for one day",
    parameters=[
        OpenApiParameter(name='username',
                         description='Enter a you username.', type=OpenApiTypes.STR),
        OpenApiParameter(name='password',
                         description='Enter a you password.', type=OpenApiTypes.STR),
    ],
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