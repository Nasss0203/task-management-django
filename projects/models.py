import uuid
import datetime
from datetime import timedelta

from django.db import models
from django.conf import settings


def default_end_date():
    return datetime.date.today() + timedelta(days=30)


class Project(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Not Started'),
        ('active', 'In Progress'),
        ('done', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Quan hệ chính
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='owned_projects',
        null=True,
        blank=True
    )
    members = models.ManyToManyField(
        'users.User',
        related_name='projects',
        blank=True
    )

    # Trạng thái và quản lý thời gian
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo', blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium',blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(default=default_end_date, blank=True)

    # Quản lý vòng đời
    is_archived = models.BooleanField(default=False)
    is_personal = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects'
