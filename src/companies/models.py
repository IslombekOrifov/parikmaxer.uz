from django.db import models

from accounts.models import CustomUser
from .services import upload_logo_path


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to=upload_logo_path)

    director = models.OneToOneField(CustomUser, on_delete=models.PROTECT, related_name='company')
    

class CompanyAdress(models.Model):
    address = models.CharField(max_length=150)
    google_map = models.URLField(max_length=500)
    tel1 = models.CharField(max_length=13)
    tel2 = models.CharField(max_length=13, blank=True, null=True)
    