from rest_framework import (
    generics, 
    permissions,
    response,
    validators
)

from accounts.models import CustomUser, Experience

from api.v1.accounts.serializers import (
    UserRegisterSerializer, UserEditSerializer,
    UserDetailSerializer, ExperienceSerializer
)


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(is_active=True, is_deleted=False)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSerializer

    def get_object(self):
        obj = CustomUser.objects.filter(
            email=self.request.user.email
        ).select_related('profile').prefetch_related('experiences').first()
        return obj
    


class UserEditAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.filter(is_active=True, is_deleted=False)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserEditSerializer

    def get_object(self):
        return CustomUser.objects.get(email=self.request.user.email)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)


class ExperienceCreateAPIView(generics.CreateAPIView):
    queryset = Experience.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExperienceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExperienceDestroyAPIView(generics.DestroyAPIView):
    queryset = Experience.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExperienceSerializer

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise validators.ValidationError("You aren't owner this experience")


class ExperienceListAPIView(generics.ListAPIView):
    queryset = Experience.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExperienceSerializer
    lookup_field = 'custom_id'

    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        queryset = Experience.objects.filter(user__custom_id=self.kwargs[lookup_url_kwarg])
        print(self.lookup_field)
        print(self.kwargs[lookup_url_kwarg])
        return queryset
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_object(self):
        return super().get_object()