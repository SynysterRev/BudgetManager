from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .default import DEFAULT_CATEGORIES
from .models import Category


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        for cat in DEFAULT_CATEGORIES:
            Category.objects.create(user=instance, name=cat["name"], color=cat["color"])
