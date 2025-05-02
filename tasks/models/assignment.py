from django.db import models
from .task import Task
import uuid
class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='assignments')  # sử dụng lazy loading
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_assignments'