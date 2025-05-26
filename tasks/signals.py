from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from projects.models import Project

@receiver(post_save, sender=Task)
def update_project_status(sender, instance, **kwargs):
    project = instance.projectId  
    if not project:
        return

    tasks = project.tasks.all()

    if not tasks.exists():
        project.status = 'todo'  
    elif tasks.filter(status='done').count() == tasks.count():
        project.status = 'done'
    elif tasks.filter(status='doing').exists() or tasks.filter(status='todo').exists():
        if tasks.filter(status='todo').count() == tasks.count():
            project.status = 'todo'
        else:
            project.status = 'active'
    else:
        project.status = 'active'


    project.save()