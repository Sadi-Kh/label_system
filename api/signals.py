from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import TextEntry, Category
from django.db import models
from django.utils import timezone


@receiver(post_save, sender=TextEntry)
def update_on_tagging(sender, instance, created, **kwargs):
    if not created:
        original = TextEntry.objects.get(pk=instance.pk)
        if original.is_tagged != instance.is_tagged:
            if instance.is_tagged:
                instance.categories.update(labeled_instances_count=models.F('labeled_instances_count') + 1)
                instance.tagged_at = timezone.now()
            else:
                instance.categories.update(labeled_instances_count=models.F('labeled_instances_count') - 1)
                instance.tagged_at = None
            instance.save(update_fields=['tagged_at'])

@receiver(m2m_changed, sender=TextEntry.categories.through)
def update_on_category_change(sender, instance, action, **kwargs):
    if action == 'post_add':
        for category in instance.categories.all():
            category.increment_labeled_instances()
    elif action == 'post_remove':
        for category in instance.categories.all():
            category.decrement_labeled_instances()

