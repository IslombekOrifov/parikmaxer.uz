from django.db import models

from utils.status import AdStatus
from accounts.models import CustomUser
from companies.models import Company
from .services import upload_ads_path


class Ad(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, 
        related_name='ads'
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=upload_ads_path)
    status = models.CharField(max_length=3, choices=AdStatus.choices, default=AdStatus.WAITING)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='ads',
        null=True
    )
    start_at = models.DateField(auto_now=True)
    end_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title