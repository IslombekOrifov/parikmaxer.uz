from django.urls import path

from api.v1.orders.views import OrderListCreateAPIView

urlpatterns = [
    path('all/', OrderListCreateAPIView.as_view(), name='order_listcreate'),
]
