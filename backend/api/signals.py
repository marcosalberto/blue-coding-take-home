from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Form

@receiver(post_save, sender=Form)
def clear_form_cache(sender, **kwargs):
    cache.clear()