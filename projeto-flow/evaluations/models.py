from django.db import models
from base.models import Base
from institution.models import Institution
import uuid 
from django.utils import timezone




class Evaluation(Base):
    submission = models.ForeignKey('submission.Submission', on_delete=models.CASCADE, related_name='submission_evaluations')
    institution = models.ForeignKey('institution.Institution', on_delete=models.CASCADE, related_name='institution_evaluations')
    proposal = models.ForeignKey('proposals.Proposal', on_delete=models.CASCADE, related_name='proposal_evaluations')
    note_scientific_relevance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nota de Relevância Científica')
    note_feasibility_methodological = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nota de Viabilidade Metodológica')
    note_expected_results = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nota de Resultados Esperados')
    score = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Pontuação Total')
    project_report = models.TextField(verbose_name='Relatório do Projeto')
    strength_points = models.TextField(verbose_name='Pontos Fortes')
    weak_points = models.TextField(verbose_name='Pontos Fracos')
    recommendations = models.TextField(verbose_name='Recomendações')
    
    def __str__(self):
        return f"Avaliação {self.pk} - Pontuação: {self.score}"

class Reviewer(Base):
    """
    Modelo para representar um avaliador.
    """
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name="Instituição Vinculada")
    name = models.CharField(max_length=200, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="E-mail", unique=True)
    cpf = models.CharField(max_length=14, verbose_name="CPF", unique=True)
    expertise = models.CharField(max_length=200, verbose_name="Área de Atuação")

    def __str__(self):
        return self.name
    
class ReviewerInvite(models.Model):
    email = models.EmailField(verbose_name="E-mail do Convidado", unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Token único para o convite
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.email