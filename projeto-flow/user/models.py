from django.db import models
from base.models import Base
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    cpf = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("CPF")
    )
    phone = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        verbose_name=_("Telefone")
    )
    address = models.ForeignKey(
        'address.Address',
        on_delete=models.SET_NULL,
        related_name='users',
        blank=True,
        null=True,
        verbose_name=_("Endereço")
    )

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def __str__(self):
        return self.username

class Profile(Base):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuário'
    )

    class Role(models.TextChoices):
        RESEARCHER = "researcher", _("Pesquisador")
        MANAGER = "manager", _("Gerente")
        EVALUATOR = "evaluator", _("Avaliador")

    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        verbose_name=_("Cargo"),
        db_index=True,
    )

    def __str__(self):
        return self.user.username