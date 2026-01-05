from django.db import models
from base.models import Base
from django.conf import settings


class Institution(Base):
    name = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=24, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    
    address = models.ForeignKey(
        'address.Address',
        on_delete=models.CASCADE,
        related_name='institutions',
        blank=True,
        null=True
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_institutions',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name