from django.db import models
from base.models import Base
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Profile(Base):
    """
    Modelo para estender o User nativo do Django com dados extras.
    Relação One-to-One: cada User tem um Profile.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuário'
    )
    cpf = models.CharField(
        max_length=14,
        blank=True, null=True
    )
    phone = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )
    address = models.ForeignKey(
        'address.Address',
        on_delete=models.CASCADE,
        related_name='profiles',
        blank=True,
        null=True
    )    


    class Role(models.TextChoices):
        RESEARCHER = "researcher", _("Pesquisador")
        MANAGER = "manager", _("Gerente")
        USER = "user", _("Usuário Comum")
        EVALUATOR = "evaluator", _("Avaliador")
    
    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        default=Role.USER,
        verbose_name=_("Cargo"),
        db_index=True,
    )

    def __str__(self):
        return self.user.username