from django.db import models
from base.models import Base


class Proposal(Base):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    departament = models.CharField(max_length=100, verbose_name='Departamento')
    proprsal_file = models.FileField(upload_to='institutions/', null=True, blank=True, verbose_name='Arquivo')

    def __str__(self):
        return self.title
    
class RectifyProposal(Base):
    id = models.AutoField(primary_key=True)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='rectifications')
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    departament = models.CharField(max_length=100, verbose_name='Departamento')
    rectify_file = models.FileField(upload_to='institutions/', null=True, blank=True, verbose_name='Arquivo')

    def __str__(self):
        return self.title