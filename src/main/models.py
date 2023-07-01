from uuid import uuid4
from django.db import models
from django.utils.text import slugify

from utils.status import Status1
from accounts.models import CustomUser
from .validators import validate_news_image
from .services import upload_news_path


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(
        upload_to=upload_news_path, 
        validators=[validate_news_image], 
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