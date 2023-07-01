from rest_framework import generics, permissions

from companies.models import CompanyBranch, CompanyService
from orders.models import Order

from api.v1.orders.serializers import OrderSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        return orders
