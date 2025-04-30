# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import User
from .serializers import UserSerializer

class UserListView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
