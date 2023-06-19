from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer

from accounts.models import CustomUser


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer