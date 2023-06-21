from rest_framework import generics, permissions

from accounts.models import CustomUser

from api.v1.accounts.serializers import UserRegisterSerializer



class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer