from django.db import models
from base.models import Base


class Proposal(Base):
    institution = models.ForeignKey('institutions.Institution', on_delete=models.CASCADE, related_name='proposals')
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    target = models.TextField(verbose_name='Objetivo')
    opening_date = models.DateField(verbose_name='Data de Abertura')
    closing_date = models.DateField(verbose_name='Data de Fechamento')
    research = models.ForeignKey('pesquisador.Researcher', on_delete=models.CASCADE, related_name='proposals')
    submissions = models.ForeignKey('submissions.Submission', on_delete=models.CASCADE, related_name='proposals', null=True, blank=True)
    proposal_file = models.FileField(upload_to='proposals/', null=True, blank=True, verbose_name='Arquivo')

    def __str__(self):
        return self.title
    
class RectifyProposal(Base):
    research = models.ForeignKey('pesquisador.Researcher', on_delete=models.CASCADE, related_name='proposals')
    institution = models.ForeignKey('institutions.Institution', on_delete=models.CASCADE, related_name='proposals')
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    target = models.TextField(verbose_name='Objetivo')
    opening_date = models.DateField(verbose_name='Data de Abertura')
    closing_date = models.DateField(verbose_name='Data de Fechamento')
    rectify_file = models.FileField(upload_to='proposals/', null=True, blank=True, verbose_name='Arquivo')

    def __str__(self):
        return self.title