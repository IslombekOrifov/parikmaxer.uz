from django.contrib import admin

from .models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['company', 'author', 'title', 'image', 'status', 'start_at', 'end_at', 'created_at']