from django.db import models
from base.models import Base


class Proposal(Base):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    departament = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)
    proprsal_file = models.FileField(upload_to='subimissions/', null=True, blank=True)

    def __str__(self):
        return self.title