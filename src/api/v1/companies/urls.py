from django.urls import path

from .views import (
    CompanyListApiView, CompanyUpdateApiView, CompanyDestroyAPIView,
    CompanyBranchListCreateApiView, CompanyBranchUpdateApiView,

)

urlpatterns = [
    # company urls
    path('list/', CompanyListApiView.as_view(), name='company_list'),
    path('update/<slug:slug>/', CompanyUpdateApiView.as_view(), name='company_update'),
    path('destroy/<slug:slug>/', CompanyDestroyAPIView.as_view(), name='company_update'),

    # company branch urls
    path('branch/create/<slug:slug>/', CompanyBranchListCreateApiView.as_view(), name='companybranch_list'),
    path('branch/update/<slug:slug>/', CompanyBranchUpdateApiView.as_view(), name='companybranch_update'),
    path('branch/list/', CompanyBranchListCreateApiView.as_view(), name='companybranch_create'),

]
