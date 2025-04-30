from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    ]

    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'

