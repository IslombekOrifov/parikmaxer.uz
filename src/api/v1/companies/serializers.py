from uuid import uuid4
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from companies.models import (
    Company,
    CompanyBranch,
    CompanyWorker,
    CompanyService,
    ServiceImage,
    Rating
)

    
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['created_at', 'updated_at',]
        extra_kwargs = {
            'slug': {'read_only': True},
            'director': {'read_only': True},
        }

    
class CompanyBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBranch
        exclude = ['created_at', 'updated_at']
        extra_kwargs = {
            'company': {'read_only': True},
            'slug': {'read_only': True},
        }


class CompanyWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyWorker
        fields = ['user',]

    
class CompanyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyService
        exclude = ['created_at', 'company_branch',]
        extra_kwargs = {
            'slug': {'read_only': True},
            'director': {'read_only': True},
        }

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['image',]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate', 'description']