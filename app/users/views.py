from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
