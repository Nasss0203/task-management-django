from django.db import models

class Notification(models.Model):
    READ_STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read')
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read_status = models.CharField(max_length=10, choices=READ_STATUS_CHOICES, default='unread')
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
