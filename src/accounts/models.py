from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils.text import slugify
from uuid import uuid4

from utils.status import Gender, Status1
from .validators import validate_phone, validate_image
from .services import upload_avatar_path, upload_news_path


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(
        max_length=13, 
        blank=True, 
        validators=[validate_phone]
    )
    custom_id = models.CharField(
        max_length=12,
        db_index=True,
        error_messages={
            "unique": _("A user with that custom_id already exists."),
        },
        unique=True,
    )

    image = models.ImageField(
        upload_to=upload_avatar_path, 
        validators=[validate_image], 
        blank=True, null=True
    )
    gender = models.CharField(
        max_length=2, 
        choices=Gender.choices, 
        default=Gender.NONE
    )    
    is_worker = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()}"
        return f'{self.email}'
    

    def save(self, *args, **kwargs):
        self.email = ' '.join(self.email.strip().split())
        self.phone = ' '.join(self.phone.strip().split())
        if self.custom_id == '':
            self.custom_id = str(uuid4())[-12:]
        super().save(*args, **kwargs)


class Profile(models.Model):
    """ User's profile datas """

    class LifeStatus(models.TextChoices):
        SINGLE = 's', 'Single'
        RELATIONSHIP = 'ir', 'In relationship'

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    about = models.CharField(max_length=300, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    skills = models.CharField(max_length=300, blank=True)
    overview = models.CharField(max_length=100, blank=True)    
    life_status = models.CharField(
        max_length=2, 
        choices=LifeStatus.choices, 
        default=LifeStatus.SINGLE
    )

    def __str__(self):
        return f"{self.user.email} > profile"
    

class Experience(models.Model):
    user = models.ForeignKey(CustomUser, related_name='experiences', on_delete=models.CASCADE)
    
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    work_start_date = models.DateField()
    work_end_date = models.DateField(blank=True, null=True)
    work_now = models.BooleanField(default=False)
    work_duties = models.CharField(max_length=300, blank=True)

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.role
    

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(
        upload_to=upload_news_path, 
        validators=[validate_image], 
        blank=True, null=True
    )
    body = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(max_length=3, choices=Status1.choices, default=Status1.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.body != '':
            self.body = ' '.join(self.body.strip().split())
        if self.title != '':
            self.title = ' '.join(self.title.strip().split())
        if not self.slug:
            self.slug == slugify(uuid4())
        super().save(self, *args, **kwargs)