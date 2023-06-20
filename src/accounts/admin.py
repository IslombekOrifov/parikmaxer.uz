from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Profile, Experience, News
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets+ (
        (      
            'Custom fields', # you can also use None                 
            {
                'fields': (
                    'custom_id',
                    'phone',
                    'image',
                    'gender',
                    'is_worker',
                    'is_company',
                    'is_deleted',
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'life_status']
    

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'company' 'created_at']
    

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'slug', 'image' 'status', 'created_at']