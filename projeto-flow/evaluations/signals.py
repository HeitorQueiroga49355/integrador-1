from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from proposals.models import Proposal
from .services import auto_distribute_on_proposal_close
from datetime import date


@receiver(pre_save, sender=Proposal)
def check_proposal_closing(sender, instance, **kwargs):
    """
    Signal que verifica se o edital está sendo fechado.
    Se a data de fechamento mudou para hoje ou passou, 
    pode disparar a distribuição automática.
    """
    if instance.pk:  # Se o edital já existe
        try:
            old_instance = Proposal.objects.get(pk=instance.pk)
            
            # Verifica se o edital acabou de ser fechado
            today = date.today()
            was_open = old_instance.closing_date >= today
            is_closed = instance.closing_date < today
            
            # Armazena flag para usar no post_save
            if was_open and is_closed:
                instance._just_closed = True
            
        except Proposal.DoesNotExist:
            pass


@receiver(post_save, sender=Proposal)
def auto_distribute_on_close(sender, instance, created, **kwargs):
    """
    Após salvar um edital, se ele acabou de fechar,
    distribui automaticamente as submissões.
    
    IMPORTANTE: Você pode ativar/desativar essa distribuição automática
    comentando ou descomentando este signal. Se preferir distribuição manual,
    comente todo este signal.
    """
    # PARA DISTRIBUIÇÃO AUTOMÁTICA
    if hasattr(instance, '_just_closed') and instance._just_closed:
        # Aguarda 1 segundo para garantir que todas as submissões foram processadas
        from django.db import transaction
        transaction.on_commit(lambda: auto_distribute_on_proposal_close(instance.id))
    
    # pass  # PARA DISTRIBUIÇÃO MANUAL, COMENTE COMENTE O SINAL ACIMA E DESCOMENTE ESTA LINHA