from django.urls import path
from .views import UserListView,UserCreateView, UserLoginView, UserLogoutView
urlpatterns = [
    path('list-user/', UserListView.as_view(), name='fetch-all-users'),
    path('create/', UserCreateView.as_view(), name='Create user'),
    path('login/', UserLoginView.as_view(), name='Create user'),
    path('logout/', UserLogoutView.as_view(), name='Create user'),
]
