from django.db import models

from utils.status import OrderStatus
from accounts.models import CustomUser
from companies.models import (
    CompanyBranch, 
    CompanyService, 
    CompanyWorker
)


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    company_branch = models.ForeignKey(
        CompanyBranch, 
        on_delete=models.CASCADE,
        related_name='orders'
    )
    service = models.ForeignKey(
        CompanyService,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    worker = models.ForeignKey(
        CompanyWorker, 
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=2,
        choices=OrderStatus.choices,
        default=OrderStatus.WAITING
    )
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s order"