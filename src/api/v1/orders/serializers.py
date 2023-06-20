from uuid import uuid4
from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'company_branch': {'read_only': True},
            
        }