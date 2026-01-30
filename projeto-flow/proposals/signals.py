from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from proposals.models import Proposal, Version

@receiver(post_save, sender=Version)
def update_submission_version(sender, instance, created, **kwargs):
    """
    Sempre que uma nova retificação (Version) for criada, 
    atualiza o número da versão na Submission pai.
    """
    if created:
        proposal = instance.proposal
        proposal.version += 1

        proposal.save()