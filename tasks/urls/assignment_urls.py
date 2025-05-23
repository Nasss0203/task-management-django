from django.urls import path
from tasks.views.assignment_views import (AssignTaskView,AssignmentListByTaskView,UserAssignmentsView, DeleteAssignmentView )

urlpatterns = [
    path('', AssignTaskView.as_view(), name='assignment-create'),
    path('task/<str:task_id>/', AssignmentListByTaskView.as_view(), name='assignment-list-by-task'),
    path('user/<str:user_id>/', UserAssignmentsView.as_view(), name='user-assignments'),
    path('delete/', DeleteAssignmentView.as_view(), name='delete-assignments'),
]
