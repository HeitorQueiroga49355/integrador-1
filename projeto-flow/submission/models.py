from django.db import models
from base.models import Base


class Submission(Base):
    """
    Modelo para representar uma submissão de proposta.
    Relação Many-to-One: cada Researcher pode ter múltiplas Submissions.
    """
    proposal = models.ForeignKey('proposals.Proposal', on_delete=models.CASCADE, related_name='submissions_list')
    researcher = models.ForeignKey('pesquisador.Researcher', on_delete=models.CASCADE, related_name='submissions_researcher')
    title = models.CharField(max_length=255, verbose_name='Título da Submissão')
    abstract = models.TextField(verbose_name='Resumo')
    keywords = models.CharField(max_length=255, verbose_name='Palavras-chave')
    justification = models.TextField(verbose_name='Justificativa')
    methodology = models.TextField(verbose_name='Metodologia')
    project_timeline = models.TextField(verbose_name='Cronograma do Projeto')
    project_budget = models.TextField(verbose_name='Orçamento do Projeto')
    expected_results = models.TextField(verbose_name='Resultados Esperados')
    status = models.CharField(max_length=50, verbose_name='Status da Submissão')
    version = models.IntegerField(default=1, verbose_name='Versão da Submissão')
    evaluation_score = models.ForeignKey('evaluations.Evaluation', on_delete=models.SET_NULL, null=True, blank=True, related_name='submissions', verbose_name='Avaliação')
    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True, verbose_name='Arquivo da Submissão')

    def __str__(self):
        return self.title


class Version(Base):
    """
    Modelo para representar uma retificação de submissão.
    Relação Many-to-One: cada Submission pode ter múltiplas RectifySubmissions.
    """
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
    rectify_file = models.FileField(upload_to='submissions/rectifications/', null=True, blank=True, verbose_name='Arquivo da Retificação')

    def __str__(self):
        return self.title