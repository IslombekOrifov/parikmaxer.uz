from django.urls import path

from api.v1.ads.views import AdListApiView

urlpatterns = [
    path('list/', AdListApiView.as_view(), name='ads_list'),
]
