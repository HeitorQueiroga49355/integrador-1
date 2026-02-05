from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile for every new User.
    Defaults to researcher role if no profile exists.
    """
    if created:
        # Only create profile if it doesn't exist
        if not hasattr(instance, 'profile'):
            Profile.objects.get_or_create(
                user=instance,
                defaults={'role': Profile.Role.RESEARCHER}
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the profile when the user is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
