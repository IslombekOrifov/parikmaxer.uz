from rest_framework import (
    generics, 
    permissions,
    validators,
    response,
    status
)

from utils.status import Status1
from companies.models import (
    ApplicationCompany, Company,
    CompanyBranch,
    Rating
)

from api.v1.companies.serializers import (
    CompanySerializer, CompanyRetrieveSerializer, CompanyBranchSerializer,
    CompanyBranchRetrieveSerializer,
    RatingSerializer
)


class CompanyRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanyRetrieveSerializer
    lookup_field = 'slug'

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = Company.objects.filter(**filter_kwargs).prefetch_related('branches')

        self.check_object_permissions(self.request, obj)
        return obj
    

class CompanyUpdateApiView(generics.UpdateAPIView):
    queryset = Company.objects.filter(is_deleted=False)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanySerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if request.user != instance.user:
            raise validators.ValidationError("Its not your company")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return response.Response(serializer.data)


class CompanyListApiView(generics.ListAPIView):
    queryset = Company.objects.filter(status=Status1.ACTIVE)
    permission_classes = (permissions.AllowAny,)
    serializer_class = CompanySerializer


class CompanyDestroyAPIView(generics.DestroyAPIView):
    queryset = Company.objects.filter(is_deleted=False)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanySerializer
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            instance.is_deleted = True
            instance.save()
        else:
            raise validators.ValidationError("You can't delete this company. It's not your!")
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    

class CompanyBranchListCreateApiView(generics.ListCreateAPIView):
    queryset = CompanyBranch.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CompanyBranchSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        queryset = CompanyBranch.objects.filter(company__slug=self.kwargs[lookup_url_kwarg])
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


class CompanyBranchUpdateApiView(generics.UpdateAPIView):
    queryset = CompanyBranch.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanyBranchSerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.company != request.user.company:
            raise validators.ValidationError("You can't update this company's branch. It's not your!")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)
    

class CompanyBranchDestroyAPIView(generics.DestroyAPIView):
    queryset = CompanyBranch.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanySerializer
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.company == request.user.company:
            instance.delete()
        else:
            raise validators.ValidationError("You can't delete this company's branch. It's not your!")
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class CompanyBranchRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanyBranchRetrieveSerializer
    lookup_field = 'slug'

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = CompanyBranch.objects.filter(**filter_kwargs).prefetch_related('services', 'workers')

        self.check_object_permissions(self.request, obj)
        return obj
    


class RatingCreateAPIView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RatingSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        
        assert self.lookup_field in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, self.lookup_field)
        )
        c_query = Company.objects.filter(status=Status1.ACTIVE)
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = generics.get_object_or_404(c_query, **filter_kwargs)
        
        serializer.save(user=self.request.user, company=obj)