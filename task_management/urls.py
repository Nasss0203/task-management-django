from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('api/users/', include('users.urls')),
    # path(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]


