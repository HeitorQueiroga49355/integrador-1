from django.db import models
from base.models import Base
from institution.models import Institution


class Researcher(models.Model):
    """
    Modelo para representar um pesquisador.
    Relação One-to-One: cada Researcher está associado a um User.
    """
    user = models.OneToOneField(
        'auth.User', 
        on_delete=models.CASCADE,
        related_name='researcher_profile',
        verbose_name='Usuário'
    )

    def __str__(self):
        return f"{self.user.username}"

class Project(Base):
    # Dados Gerais
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE, related_name='project_researcher')
    Institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='projeto_campus')
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='projeto_course')
    title = models.CharField(max_length=255, verbose_name='Titulo')
    weekly_workload = models.IntegerField(verbose_name='Carga Horaria')
    # Dados do Projeto
    start_date = models.DateField(verbose_name='Data de Inicio')
    end_date = models.DateField(verbose_name='Data de Fim')
    total_workload = models.IntegerField(verbose_name='Carga Horaria Total')
    thematic_axis = models.CharField(max_length=255, verbose_name='Eixo Tematico')
    interdisciplinary_project = models.BooleanField(verbose_name='Projeto Interdisciplinar')
    disciplines = models.CharField(max_length=255, verbose_name='Disciplinas')
    courses = models.CharField(max_length=255, verbose_name='Cursos')
   
    # Adição do Projeto
    project_file = models.FileField(upload_to='projects/', null=True, blank=True, verbose_name='Arquivo')

    def __str__(self):
        return self.title
