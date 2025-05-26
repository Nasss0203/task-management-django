from django.urls import path
from .views import (
ProjectMessView
)

urlpatterns = [
    path('projects/<str:project_id>/', ProjectMessView.as_view(), name='project-messages'),
 
]
