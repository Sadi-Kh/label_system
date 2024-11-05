from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Dataset(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_entries(self):
        return self.text_entries.count()

    @property
    def tagged_entries(self):
        return self.text_entries.filter(is_tagged=True).count()

    def __str__(self):
        return self.title


class Category(models.Model):
    dataset = models.ForeignKey('Dataset', related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    labeled_instances_count = models.PositiveIntegerField(default=0)

    def filtered_entries_count(self, start_date=None, end_date=None, tagged_by=None):
        entries = self.textentry_set.filter(is_tagged=True)

        if start_date:
            entries = entries.filter(tagged_at__gte=start_date)
        if end_date:
            entries = entries.filter(tagged_at__lte=end_date)
        if tagged_by:
            entries = entries.filter(tagged_by=tagged_by)

        return entries.count()

    def increment_labeled_instances(self):
        self.labeled_instances_count += 1
        self.save()

    def decrement_labeled_instances(self):
        if self.labeled_instances_count > 0:
            self.labeled_instances_count -= 1
            self.save()

    def __str__(self):
        return f"{self.name} (Active: {self.is_active})"


class TextEntry(models.Model):
    content = models.TextField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='text_entries')
    categories = models.ManyToManyField(Category, blank=True)
    is_tagged = models.BooleanField(default=False)
    tagged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tagged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_tagged:
            self.tagged_at = timezone.now()
        else:
            self.tagged_at = None
        super().save(*args, **kwargs)

class Operator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    datasets = models.ManyToManyField(Dataset, related_name='operators')

    def tagged_entries_in_period(self, start_date, end_date):
        return TextEntry.objects.filter(
            tagged_by=self.user,
            tagged_at__range=[start_date, end_date]
        ).count()

