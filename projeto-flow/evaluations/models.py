from django.db import models
from base.models import Base
from institution.models import Institution

class Reviewer(Base):
    """
    Modelo para representar um avaliador.
    """
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name="Instituição Vinculada")
    name = models.CharField(max_length=200, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="E-mail", unique=True)
    cpf = models.CharField(max_length=14, verbose_name="CPF", unique=True)
    expertise = models.CharField(max_length=200, verbose_name="Área de Atuação")
    
    # Novo campo para vincular avaliador ao usuário (se necessário)
    user = models.OneToOneField(
        'user.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewer_profile',
        verbose_name="Usuário do Sistema"
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Avaliador"
        verbose_name_plural = "Avaliadores"


class SubmissionAssignment(Base):
    """
    Modelo para representar a atribuição de uma submissão a um avaliador.
    Permite rastrear quando e por quem a distribuição foi feita.
    """
    submission = models.ForeignKey(
        'submission.Submission',
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Submissão"
    )
    reviewer = models.ForeignKey(
        Reviewer,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Avaliador"
    )
    assigned_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Atribuição"
    )
    assigned_by = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assignments_made',
        verbose_name="Atribuído por"
    )
    notified = models.BooleanField(
        default=False,
        verbose_name="Avaliador Notificado?"
    )
    notified_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data da Notificação"
    )
    
    class Meta:
        verbose_name = "Atribuição de Avaliação"
        verbose_name_plural = "Atribuições de Avaliações"
        unique_together = ['submission', 'reviewer']  # Evita duplicatas
    
    def __str__(self):
        return f"{self.reviewer.name} -> {self.submission.title}"


class Evaluation(Base):
    """
    Modelo para armazenar a avaliação feita por um avaliador.
    """
    assignment = models.OneToOneField(
        SubmissionAssignment,
        on_delete=models.CASCADE,
        related_name='evaluation',
        verbose_name="Atribuição",
        null=True,
        blank=True
    )
    submission = models.ForeignKey(
        'submission.Submission',
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name="Submissão"
    )
    reviewer = models.ForeignKey(
        Reviewer,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name="Avaliador"
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='institution_evaluations',
        verbose_name="Instituição"
    )
    proposal = models.ForeignKey(
        'proposals.Proposal',
        on_delete=models.CASCADE,
        related_name='proposal_evaluations',
        verbose_name="Edital"
    )
    
    # Notas
    note_scientific_relevance = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Nota de Relevância Científica',
        null=True,
        blank=True
    )
    note_feasibility_methodological = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Nota de Viabilidade Metodológica',
        null=True,
        blank=True
    )
    note_expected_results = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Nota de Resultados Esperados',
        null=True,
        blank=True
    )
    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Pontuação Total',
        null=True,
        blank=True
    )
    
    # Pareceres
    project_report = models.TextField(
        verbose_name='Relatório do Projeto',
        blank=True,
        null=True
    )
    strength_points = models.TextField(
        verbose_name='Pontos Fortes',
        blank=True,
        null=True
    )
    weak_points = models.TextField(
        verbose_name='Pontos Fracos',
        blank=True,
        null=True
    )
    recommendations = models.TextField(
        verbose_name='Recomendações',
        blank=True,
        null=True
    )
    
    # Status da avaliação
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluída'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status da Avaliação'
    )
    
    completed_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Conclusão"
    )
    
    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ['submission', 'reviewer']
    
    def __str__(self):
        return f"Avaliação de {self.reviewer.name} - {self.submission.title}"
    
    def save(self, *args, **kwargs):
        # Calcula o score automaticamente
        if all([
            self.note_scientific_relevance is not None,
            self.note_feasibility_methodological is not None,
            self.note_expected_results is not None
        ]):
            self.score = (
                self.note_scientific_relevance +
                self.note_feasibility_methodological +
                self.note_expected_results
            )
            
            # Se todas as notas estão preenchidas, marca como concluída
            if self.project_report and self.status == 'pending':
                self.status = 'completed'
                if not self.completed_date:
                    from django.utils import timezone
                    self.completed_date = timezone.now()
        
        super().save(*args, **kwargs)