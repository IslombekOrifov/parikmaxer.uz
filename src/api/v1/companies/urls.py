from django.urls import path

from .views import (
    CompanyListApiView, CompanyUpdateApiView, CompanyDestroyAPIView,
    CompanyBranchListCreateApiView, CompanyBranchUpdateApiView,
    CompanyBranchDestroyAPIView,
    CompanyWorkerListCreateAPIView, CompanyWorkerDestroyAPIView,
    CompanyServiceCreateAPIView, CompanyServiceUpdateApiView,
    CompanyServiceListAPIView, CompanyServiceDestroyAPIView,

    ServiceWorkersAPIView,

)

urlpatterns = [
    # company urls
    path('list/', CompanyListApiView.as_view(), name='company_list'),
    path('update/<slug:slug>/', CompanyUpdateApiView.as_view(), name='company_update'),
    path('destroy/<slug:slug>/', CompanyDestroyAPIView.as_view(), name='company_destroy'),

    # company branch urls
    path('branch/create/<slug:slug>/', CompanyBranchListCreateApiView.as_view(), name='companybranch_list'),
    path('branch/update/<slug:slug>/', CompanyBranchUpdateApiView.as_view(), name='companybranch_update'),
    path('branch/destroy/<slug:slug>/', CompanyBranchDestroyAPIView.as_view(), name='companybranch_destroy'),
    path('branch/list/<slug:slug>/', CompanyBranchListCreateApiView.as_view(), name='companybranch_create'),

    # company worker urls
    path('worker/create/<slug:slug>/', CompanyWorkerListCreateAPIView.as_view(), name='companyworker_create'),
    path('worker/list/<slug:slug>/', CompanyWorkerListCreateAPIView.as_view(), name='companyworker_list'),
    path('workers/destroy<int:pk>/', CompanyWorkerDestroyAPIView.as_view(), name='companyworker_destroy'),

    # company service urls
    path('service/create/<slug:slug>/', CompanyServiceCreateAPIView.as_view(), name='companyservice_create'),
    path('service/update/<int:pk>/', CompanyServiceUpdateApiView.as_view(), name='companyservice_update'),
    path('service/list/<slug:slug>/', CompanyServiceListAPIView.as_view(), name='companyservice_list'),
    path('service/destroy/<int:pk>/', CompanyServiceDestroyAPIView.as_view(), name='companyservice_destroy'),

    path('service/worker/<int:pk>/', ServiceWorkersAPIView.as_view(), name='service_workers'),
]
