from uuid import uuid4
from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user', 'company_branch', 'service', 'worker', 'status', 'description', 'created_at', 'updated_at')
        extra_kwargs = {
            'user': {'read_only': True},
            'status': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }