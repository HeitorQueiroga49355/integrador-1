from django.db import models
from base.models import Base


class Address(Base):
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    neighborhood = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    street_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.street}, {self.street_number} - {self.city}/{self.state}"