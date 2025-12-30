from django.db import models


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