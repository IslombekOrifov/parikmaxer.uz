from django.contrib import admin

from .models import (
    News,
)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'slug', 'image', 'status', 'created_at']