from django.db import models

from utils.status import PersonCategory, Status1, ReciveStatus
from accounts.models import CustomUser
from accounts.validators import validate_phone
from .services import upload_logo_path, upload_serv_image_path


class ApplicationCompany(models.Model):
    name = models.CharField(max_length=200, unique=True)
    logo = models.ImageField(upload_to=upload_logo_path, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='application')
    person_category = models.CharField(
        max_length=3, 
        choices=PersonCategory.choices,
        default=PersonCategory.ALL
    )
    status = models.CharField(
        max_length=3,
        choices=ReciveStatus.choices,
        blank=True,
        default=ReciveStatus.WAITING
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name 


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to=upload_logo_path)
    
    director = models.OneToOneField(CustomUser, on_delete=models.PROTECT, related_name='company')
    person_category = models.CharField(
        max_length=3, 
        choices=PersonCategory.choices,
        default=PersonCategory.ALL
    )
    status = models.CharField(
        max_length=3,
        choices=Status1.choices,
        blank=True,
        default=Status1.ACTIVE
    )
    overview = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name 
    

class CompanyBranch(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, 
        related_name='branches'
    )
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    phone1 = models.CharField(
        max_length=13, 
        blank=True, 
        validators=[validate_phone]
    )
    phone2 = models.CharField(
        max_length=13, 
        blank=True, 
        validators=[validate_phone]
    )
    logo = models.ImageField(upload_to=upload_logo_path)
    address = models.CharField(max_length=150)
    google_map = models.URLField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{ self.company.name } > filial >{ self.name }" 


class CompanyWorker(models.Model):
    company_branch = models.ForeignKey(
        CompanyBranch, 
        on_delete=models.CASCADE,
        related_name='workers'
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='workers'
    )
    def __str__(self):
        return f"{ self.company_branch.company.name } > { self.worker.email }" 


class CompanyService(models.Model):
    company_branch = models.ForeignKey(
        CompanyBranch, 
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=200, db_index=True)
    person_category = models.CharField(
        max_length=3, 
        choices=PersonCategory.choices,
        default=PersonCategory.NONE
    )
    price = models.PositiveIntegerField(blank=True)
    description = models.TextField()

    workers = models.ManyToManyField(
        CompanyWorker, 
        related_name='services', 
        blank=True, 
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.company_branch.company.name } >{ self.name }" 


class ServiceImage(models.Model):
    service = models.ForeignKey(
        CompanyService,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to=upload_serv_image_path)

    def __str__(self):
        return f"{ self.service.name } > image" 


class Rating(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='ratigns',
        null=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    rate = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.user.email } > { self.company.name }" 