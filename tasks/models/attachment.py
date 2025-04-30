from django.db import models
from .task import Task

class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file_path = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    uploadedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_attachments'