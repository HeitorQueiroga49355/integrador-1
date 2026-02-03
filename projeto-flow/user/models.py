from django.db import models
from base.models import Base
from django.contrib.auth.models import AbstractUser
import os
import uuid
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


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

@deconstructible
class UploadToPath:
    """Classe para definir caminhos de upload com mais controle"""
    def __init__(self, subfolder):
        self.subfolder = subfolder
    
    def __call__(self, instance, filename):
        # Obtém a extensão do arquivo
        ext = os.path.splitext(filename)[1].lower()
        
        # Gera um nome único
        unique_id = uuid.uuid4().hex[:8]
        
        # Usa o ID do usuário para evitar colisões
        user_id = str(instance.user.id)
        
        # Nome do arquivo: user-{id}-{unique_id}{ext}
        new_filename = f"user-{user_id}-{unique_id}{ext}"
        
        # Retorna o caminho completo
        return os.path.join(self.subfolder, new_filename)


def validate_image_extension(value):
    """Valida a extensão da imagem"""
    import os
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    
    if ext not in valid_extensions:
        raise ValidationError(
            _('Formato de arquivo não suportado. Use: JPG, JPEG, PNG, GIF, WEBP ou BMP.')
        )


def validate_image_size(value):
    """Valida o tamanho da imagem (max 5MB)"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError(_("A imagem não pode ser maior que 5MB."))


class Profile(Base):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='User'
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
    
    # Campo para imagem de perfil com validações
    profile_picture = models.ImageField(
        upload_to=UploadToPath('profile_pictures'),  # Usa a classe personalizada
        blank=True,
        null=True,
        verbose_name=_("Foto de Perfil"),
        help_text=_("Formatos: JPG, JPEG, PNG, GIF, WEBP, BMP. Tamanho máximo: 5MB."),
        validators=[validate_image_extension, validate_image_size]
    )

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        # Deleta a imagem antiga se estiver atualizando
        try:
            old_instance = Profile.objects.get(pk=self.pk)
            if old_instance.profile_picture and old_instance.profile_picture != self.profile_picture:
                old_instance.profile_picture.delete(save=False)
        except Profile.DoesNotExist:
            pass
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Deleta a imagem ao deletar o perfil
        if self.profile_picture:
            self.profile_picture.delete(save=False)
        super().delete(*args, **kwargs)
    
    @property
    def profile_picture_url(self):
        """Retorna a URL da imagem ou uma imagem padrão"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/images/default-avatar.png'

    def __str__(self):
        return self.user.username