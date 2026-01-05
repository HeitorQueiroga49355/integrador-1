from django.db import models
from base.models import Base


class Proposal(Base):
    institution = models.ForeignKey('institution.Institution', on_delete=models.CASCADE, related_name='institution_proposals', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Título', blank=True, null=True)
    description = models.TextField(verbose_name='Descrição', blank=True, null=True)
    target = models.TextField(verbose_name='Objetivo', blank=True, null=True)
    opening_date = models.DateField(verbose_name='Data de Abertura', blank=True, null=True)
    closing_date = models.DateField(verbose_name='Data de Fechamento', blank=True, null=True)
    researcher = models.ForeignKey('pesquisador.Researcher', on_delete=models.CASCADE, related_name='researcher_proposals')
    submissions = models.ForeignKey('submission.Submission', on_delete=models.CASCADE, related_name='proposals', null=True, blank=True)
    proposal_file = models.FileField(upload_to='proposals/', null=True, blank=True, verbose_name='Arquivo')

    def __str__(self):
        return self.title
    
class Version(Base):
    researcher = models.ForeignKey('pesquisador.Researcher', on_delete=models.CASCADE, related_name='rectify_researcher_proposals')
    institution = models.ForeignKey('institution.Institution', on_delete=models.CASCADE, related_name='rectify_institution_proposals')
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    target = models.TextField(verbose_name='Objetivo')
    opening_date = models.DateField(verbose_name='Data de Abertura')
    closing_date = models.DateField(verbose_name='Data de Fechamento')
    rectify_file = models.FileField(upload_to='proposals/', null=True, blank=True, verbose_name='Arquivo')

    def __str__(self):
        return self.title