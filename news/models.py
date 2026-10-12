"""
Database models for the News API application.
Includes CustomeUser with RBAC, Publisher,
Article with approval signals, and Newsletter
models.
"""


import requests
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

# Create your models here.


class Publisher(models.Model):
    """Represents a news publishing organisation."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """Extends default Django user to include
    role-based access control and subscriptions."""
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')  # noqa: E501
    subscriptions_publishers = models.ManyToManyField(Publisher, blank=True, related_name='subscribers')  # noqa: E501
    subscriptions_journalists = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='journalist_subscribers')  # noqa: E501

    def __str__(self):
        return f"{self.username} ({self.role})"


@receiver(post_save, sender=CustomUser)
def sync_user_groups(sender, instance, created, **kwargs):
    """Automatically assigns users to Django Groups matching their role."""
    group_name = instance.role.capitalize()
    group, _ = Group.objects.get_or_create(name=group_name)
    instance.groups.set([group])


class Article(models.Model):
    """Represents a news article created by a
    journalist and approved by an editor."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='articles')  # noqa: E501
    journalist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles')  # noqa: E501
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Article)
def article_approval_handler(sender, instance, created, **kwargs):
    """Triggers email notifications and webhook POST
    requests when an article is approved."""
    if instance.approved and not created:
        subscribers = instance.publisher.subscribers.all()
        recipient_list = [sub.email for sub in subscribers if sub.email]

        if recipient_list:
            send_mail(
                subject=f"New Article Approved: {instance.title}",
                message=f"An article from {instance.publisher.name} has been published:\n\n{instance.content[:200]}...",  # noqa: E501
                from_email="admin@newsportal.com",
                recipient_list=recipient_list,
                fail_silently=True,
            )
        try:
            requests.post('http://127.0.0.1:8000/api/approved/', json={
                'article_id': instance.id,
                'title': instance.title,
                'publisher': instance.publisher.name
                }, timeout=3)
        except requests.RequestException:
            pass


class Newsletter(models.Model):
    """Represents aggregated newsletters compiled
    by editors or journalists."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='newsletters')  # noqa: E501
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
