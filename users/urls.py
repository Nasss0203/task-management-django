from django.urls import path
from .views import UserListView  # <-- sửa tên view ở đây

urlpatterns = [
    path('list-user/', UserListView.as_view(), name='fetch-all-users'),
]
