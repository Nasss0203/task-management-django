from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', include('tasks.urls.task_urls')),
    path('api/assignments/', include('tasks.urls.assignment_urls')),

    path('api/users/', include('users.urls')),
    path('api/projects/', include('projects.urls')),
    
]


