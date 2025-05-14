from django.urls import path

from .views import (DeleteTaskView, TaskDetailView, TaskListCreateAPIView,
                    UpdateTaskView)

urlpatterns = [
    path('create/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('<str:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('update/<str:pk>/', UpdateTaskView.as_view(), name='task-update'),
    path('delete/<str:pk>/', DeleteTaskView.as_view(), name='task-delete'),
]
