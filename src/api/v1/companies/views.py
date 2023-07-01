from rest_framework import (
    generics, 
    permissions,
    validators,
    response,
    status,
    views
)

from utils.status import Status1
from companies.models import (
    ApplicationCompany, Company,
    CompanyBranch, CompanyWorker,
    CompanyService,
    Rating
)

from api.v1.companies.serializers import (
    CompanySerializer, CompanyRetrieveSerializer, CompanyBranchSerializer,
    CompanyBranchRetrieveSerializer, CompanyWorkerSerializer,
    CompanyServiceSerializer, ServiceWorkers,
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


class CompanyWorkerListCreateAPIView(generics.ListCreateAPIView):
    queryset = CompanyWorker.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanyWorkerSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        queryset = CompanyWorker.objects.filter(
            company_branch__slug=self.kwargs[lookup_url_kwarg]
        )
        return queryset
    
    def perform_create(self, serializer):
        branch = CompanyBranch.objects.get(
            company__director=self.request.user, 
            slug=self.kwargs[self.lookup_field]
        )
        if branch:
            serializer.save(company_branch=branch)
        else:
            raise validators.ValidationError("You can't add worker to this company's branch. It's not your!")


class CompanyWorkerDestroyAPIView(generics.DestroyAPIView):
    queryset = CompanyWorker.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanyWorkerSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.company_branch.company == request.user.company:
            instance.delete()
        else:
            raise validators.ValidationError("You can't delete this worker. It's not your company!")
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class CompanyServiceListAPIView(generics.ListAPIView):
    queryset = CompanyService.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanyServiceSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        queryset = CompanyService.objects.filter(
            company_branch__slug=self.kwargs[lookup_url_kwarg]
        )
        return queryset


class CompanyServiceCreateAPIView(generics.Create):
    queryset = CompanyService.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanyServiceSerializer
    lookup_field = 'slug'
    

    def perform_create(self, serializer):
        branch = CompanyBranch.objects.get(
            company__director=self.request.user, 
            slug=self.kwargs[self.lookup_field]
        )
        if branch:
            serializer.save(company_branch=branch)
        else:
            raise validators.ValidationError("You can't add service to this company's branch. It's not your!")


class CompanyServiceUpdateApiView(generics.UpdateAPIView):
    queryset = CompanyService.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompanyServiceSerializer


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.company_branch.company != request.user.company:
            raise validators.ValidationError("You can't update this Service. It's not your!")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)


class CompanyServiceDestroyAPIView(generics.DestroyAPIView):
    queryset = CompanyService.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.company_branch.company != request.user.company:
            instance.workers.clear()
            instance.delete()
        else:
            raise validators.ValidationError("You can't delete this Service. It's not your company!")
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ServiceWorkersAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        service = CompanyService.objects.get(pk=self.kwargs.get('pk'))
        if service.exists():
            ids_list = []
            workers_ids = ServiceWorkers(data=request.data, many=True)
            if workers_ids.is_valid():
                for ids in workers_ids.data:
                    worker = CompanyWorker.objects.filter(
                        pk=ids.get('id'), 
                        company_branch__company=request.user.company
                    ).first()
                    if worker.exists():
                        ids_list.append(worker.id)
                service.workers.add(ids_list)
        return response.Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        service = CompanyService.objects.get(id=self.kwargs.get('pk'))
        ids_list = []
        if service.exists():
            workers_ids = ServiceWorkers(data=request.data)
            if workers_ids.is_valid():
                for ids in workers_ids.data:
                    worker = CompanyWorker.objects.filter(
                        pk=ids.data.get('id'), 
                        company_branch__company=request.user.company
                    ).first()
                    if worker.exists():
                        ids_list.append(worker.id)
                service.workers.remove(ids_list)
        return response.Response(status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        service = CompanyService.objects.get(id=self.kwargs.get('pk'))
        workers = CompanyWorker.objects.filter(services=service)
        serialized_data = CompanyWorkerSerializer(workers, many=True)
        return response.Response(data=serialized_data.data, status=status.HTTP_200_OK)


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