from django.db import models
from base.models import Base


class Evaluation(Base):
    """
    Modelo para representar uma avaliação de submissão.
    Relação One-to-One: cada Submission tem uma Evaluation.
    """
    institution = models.ForeignKey('institutions.Institution', on_delete=models.CASCADE, related_name='evaluations')
    proposal = models.ForeignKey('proposals.Proposal', on_delete=models.CASCADE, related_name='evaluations')
    note_scientific_relevance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nota de Relevância Científica')
    note_feasibility_mothodological = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nota de Viabilidade Metodológica')
    note_expected_results = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nota de Resultados Esperados')
    score = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Pontuação Total')
    project_report = models.TextField(verbose_name='Relatório do Projeto')
    strength_points = models.TextField(verbose_name='Pontos Fortes')
    weak_points = models.TextField(verbose_name='Pontos Fracos')
    recomendations = models.TextField(verbose_name='Recomendações')
    
    def __str__(self):
        return f"Avaliação {self.id} - Pontuação: {self.score}"
