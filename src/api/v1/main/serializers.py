from uuid import uuid4
import datetime
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from main.models import (
    News,
)

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'title', 'slug', 'image', 'body', 
            'created_at', 'author', 
        ]
