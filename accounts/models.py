from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

from .validators import validate_phone, validate_image
from .services import upload_avatar_path


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    avatar = models.ImageField(
        upload_to=upload_avatar_path, 
        validators=[validate_image], 
        blank=True, null=True
    )

    is_company = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()}"
        return f'{self.email}'
    

    def save(self, *args, **kwargs):
        if self.username:
            self.username = ' '.join(self.username.strip().split())
        self.email = ' '.join(self.email.strip().split())
        self.phone = ' '.join(self.phone.strip().split())
        super().save(*args, **kwargs)
