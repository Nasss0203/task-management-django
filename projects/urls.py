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
    RemoveTaskFromProjectView,
    ProjectTaskListView, 
    ProjectMembersView,
    MyProjectsView
)

urlpatterns = [
    path('my-projects/', MyProjectsView.as_view(), name='my-project-list'),

    path('', ProjectListView.as_view(), name='project-list'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<str:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('update/<str:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    path('delete/<str:pk>/', ProjectDeleteView.as_view(), name='project-delete'),

    # Thêm member vào project
    # Chỉ admin hoặc manager mới có quyền thêm member vào project nhóm
    path('add-member/<str:pk>/', ProjectAddMemberView.as_view(), name='project-add-member'),

    # Thêm task vào project
    path('add-tasks/<str:project_id>/', TaskCreateInProjectView.as_view(), name='task-create-in-project'),

    # Xoá thành viên khỏi project
    # Chỉ admin hoặc manager mới có quyền xoá thành viên khỏi project nhóm
    path('remove-member/<str:project_id>/', RemoveMemberFromProjectView.as_view()),

    # Xoá task khỏi project
    # Chỉ admin hoặc manager mới có quyền xoá task khỏi project nhóm
    path('remove-task/<str:project_id>/', RemoveTaskFromProjectView.as_view(), name='remove-task-from-project'),

    # Danh sách thành viên của project
    path('members/<str:project_id>/', ProjectMembersView.as_view(), name='project-members'),

]
