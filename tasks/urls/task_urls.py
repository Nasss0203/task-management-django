from django.urls import path

from tasks.views.task_views import (TaskDetailView, TaskListCreateAPIView, UpdateTaskView, DeleteTaskView, ProjectTaskListView)

urlpatterns = [
    path('', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('<str:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('update/<str:pk>/', UpdateTaskView.as_view(), name='task-update'),
    path('delete/<str:pk>/', DeleteTaskView.as_view(), name='task-delete'),
    path('projects/<str:project_id>/', ProjectTaskListView.as_view(), name='list-task-in-project'),
]


