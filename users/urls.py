from django.urls import path

from .views import (CustomLoginView, UserCreateView, UserListView,
                    UserLoginView, UserLogoutView)

urlpatterns = [
    path('list-user/', UserListView.as_view(), name='fetch-all-users'),
    path('create/', UserCreateView.as_view(), name='Create user'),
    path('login/', UserLoginView.as_view(), name='Create user'),
    path('logout/', UserLogoutView.as_view(), name='Create user'),
    path('login-custom/', CustomLoginView.as_view(), name='custom_login')

]
