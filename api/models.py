from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    parent_category_id = models.ForeignKey(
        "self",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    text = models.TextField()
    category_id = models.ForeignKey(
        Category,
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    writer_id = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
