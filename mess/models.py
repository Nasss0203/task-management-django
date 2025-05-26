from django.db import models

# Create your models here.
from django.db import models
from users.models import User
from projects.models import Project  # Import model Project

class Mess(models.Model):
    project = models.ForeignKey(
        Project,  # Liên kết tin nhắn với một project
        related_name='mess',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User,  # Người gửi tin nhắn
        related_name='sent_mess',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,  # Người nhận tin nhắn
        related_name='received_mess',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} → {self.receiver} in {self.project.name}: {self.content[:30]}"