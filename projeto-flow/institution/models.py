from django.db import models
from base.models import Base


class Institution(Base):
    name = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=24, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    neighborhood = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    manager = models.ForeignKey(
        'employee.Employee',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='manager'
    )

    def __str__(self):
        return self.name