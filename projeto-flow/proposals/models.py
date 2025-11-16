from django.db import models
from base.models import Base


class Proposal(Base):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    departament = models.CharField(max_length=100)
    proprsal_file = models.FileField(upload_to='institutions/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class RectifyProposal(Base):
    id = models.AutoField(primary_key=True)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='rectifications')
    title = models.CharField(max_length=255)
    description = models.TextField()
    departament = models.CharField(max_length=100)
    rectify_file = models.FileField(upload_to='institutions/', null=True, blank=True)

    def __str__(self):
        return self.title