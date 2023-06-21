from django.contrib import admin

from .models import (
    Company, CompanyBranch, CompanyWorker, 
    CompanyService, ServiceImage, Rating
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'logo', 'director', 'person_category', 'created_at']


@admin.register(CompanyBranch)
class CompanyBranchAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'slug', 'phone1', 'phone2', 'logo', 'address', 'google_map', 'created_at']


@admin.register(CompanyWorker)
class CompanyWorkerAdmin(admin.ModelAdmin):
    list_display = ['company_branch', 'user',]


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    list_display = ['company_branch', 'name', 'person_category', 'price', 'description', 'created_at']


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['service', 'image',]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'rate', 'created_at']