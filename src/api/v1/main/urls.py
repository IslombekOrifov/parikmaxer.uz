from django.urls import path

from api.v1.main.views import (
    NewsListAPIView,
)

urlpatterns = [
    path('news/', NewsListAPIView.as_view(), name='news'),
    
]
