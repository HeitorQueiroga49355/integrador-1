from django.db import models
from base.models import Base


class Submission(Base):
    proposal = models.ForeignKey('proposals.Proposal', on_delete=models.CASCADE, related_name='submissions_list')
    title = models.CharField(max_length=255, verbose_name='Título da Submissão')
    abstract = models.TextField(verbose_name='Resumo')
    keywords = models.CharField(max_length=255, verbose_name='Palavras-chave')
    justification = models.TextField(verbose_name='Justificativa')
    methodology = models.TextField(verbose_name='Metodologia')
    project_timeline = models.TextField(verbose_name='Cronograma do Projeto')
    project_budget = models.TextField(verbose_name='Orçamento do Projeto')
    expected_results = models.TextField(verbose_name='Resultados Esperados')
    researcher = models.ForeignKey('user.Profile', on_delete=models.CASCADE, related_name='submissions_researcher')
    status = models.CharField(max_length=50, verbose_name='Status da Submissão')
    submission_file = models.FileField(
        upload_to='submissions/',
        null=True,
        blank=True,
        verbose_name='Arquivo Principal da Submissão',
        help_text='Faça upload do arquivo PDF principal da submissão'
    )
    
    # Outros campos opcionais para anexos
    attachments = models.FileField(
        upload_to='submissions/attachments',
        null=True,
        blank=True,
        verbose_name='Anexos (opcional)',
        help_text='Anexos complementares à submissão'
    )

    def __str__(self):
        return self.title


class Version(Base):
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='rectifications_list')
    title = models.CharField(max_length=255, verbose_name='Título da Retificação')
    abstract = models.TextField(verbose_name='Resumo')
    keywords = models.CharField(max_length=255, verbose_name='Palavras-chave')
    justification = models.TextField(verbose_name='Justificativa')
    methodology = models.TextField(verbose_name='Metodologia')
    project_timeline = models.TextField(verbose_name='Cronograma do Projeto')
    project_budget = models.TextField(verbose_name='Orçamento do Projeto')
    expected_results = models.TextField(verbose_name='Resultados Esperados')
    status = models.CharField(max_length=50, verbose_name='Status da Retificação')
    file = models.FileField(upload_to='submissions/rectifications/', null=True, blank=True, verbose_name='Arquivo da Retificação')

    def __str__(self):
        return self.title