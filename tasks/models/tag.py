from django.db import models
from .task import Task
import uuid
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tags')
    tag_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'task_tags'