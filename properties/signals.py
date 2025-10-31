from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Property


@receiver(post_save, sender=Property)
def create_property(sender, instance, created, **kwargs):
    """Delete cache whenever a new Property is created."""
    if created:
        cache.delete('all_properties')

@receiver(post_delete, sender=Property)
def delete_property(sender, instance, **kwargs):
    cache.delete('all_properties')