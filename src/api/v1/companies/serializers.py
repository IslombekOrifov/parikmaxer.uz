from uuid import uuid4
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from companies.models import (
    ApplicationCompany,
    Company,
    CompanyBranch,
    CompanyWorker,
    CompanyService,
    ServiceImage,
    Rating
)


class ApplicationCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationCompany
        exclude = ("user",)
        extra_kwargs = {
            'status': {'read_only': True}
        }

    
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
        fields = [
            'company_branch', 'name', 'person_category',
            'price', 'description', 'workers'
        ]
        extra_kwargs = {
            'company_branch': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['slug'] = str(uuid4())[-15:]
        return super().create(validated_data)


class CompanyWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyWorker
        fields = ['user',]

    
class CompanyServiceSerializer(serializers.ModelSerializer):
    workers = CompanyWorkerSerializer(many=True)
    class Meta:
        model = CompanyService
        exclude = ['created_at', 'company_branch',]
        extra_kwargs = {
            'slug': {'read_only': True},
            'director': {'read_only': True},
            'workers': {'read_only': True},
        }

        def create(self, validated_data):
            validated_data['slug'] = str(uuid4())[-15:]
            return super().create(validated_data)


class ServiceWorkers(serializers.Serializer):
    id = serializers.IntegerField()


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['image',]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate', 'description']


class CompanyRetrieveSerializer(serializers.ModelSerializer):
    branches = CompanyBranchSerializer(many=True)
    class Meta:
        model = Company
        fields = [
            'name', 'slug', 'logo', 'director', 'person_category', 'status', 
            'overview', 'description', 'created_at', 'branches'
        ]


class CompanyBranchRetrieveSerializer(serializers.ModelSerializer):
    workers = CompanyWorkerSerializer(many=True)
    services = CompanyServiceSerializer(many=True)
    class Meta:
        model = CompanyBranch
        fields = [
            'company', 'name', 'slug', 'phone1', 'phone2', 'logo', 
            'address', 'google_map', 'workers', 'services'
        ]