from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from projects.models import Project

@receiver(post_save, sender=Task)
def update_project_status(sender, instance, **kwargs):
    project = instance.projectId  # Lấy project liên quan đến task
    if not project:
        return

    # Lấy tất cả các task liên quan đến project
    tasks = project.tasks.all()

    # Kiểm tra trạng thái của các task
    if tasks.filter(status='doing').exists():
        project.status = 'active'  # Đặt trạng thái project là "started"
    elif tasks.filter(status='todo').exists():
        project.status = 'todo'  # Nếu còn task "todo", project chưa bắt đầu
    elif tasks.filter(status='done').count() == tasks.count():
        project.status = 'done'  # Nếu tất cả task đều "done", project hoàn thành

    project.save()