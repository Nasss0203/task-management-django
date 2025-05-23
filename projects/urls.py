from django.urls import path
from .views import (
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
ProjectAddMemberView,
TaskCreateInProjectView,
RemoveMemberFromProjectView,
RemoveTaskFromProjectView
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<str:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('update/<str:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    path('delete/<str:pk>/', ProjectDeleteView.as_view(), name='project-delete'),


#     Add member
    path('add-member/<str:pk>/', ProjectAddMemberView.as_view(), name='project-add-member'),

#       Add task
    path('add-tasks/<str:project_id>/', TaskCreateInProjectView.as_view(), name='task-create-in-project'),

    # remove member
    path('remove-member/<str:project_id>/', RemoveMemberFromProjectView.as_view()),

    # remove task
    path('remove-task/<str:project_id>/', RemoveTaskFromProjectView.as_view(), name='remove-task-from-project'),
]
