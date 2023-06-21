from django.urls import path

from .views import AdListApiView

urlpatterns = [
    path('list/', AdListApiView.as_view(), name='ads_list'),
]
