from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Mess
from .serializers import MessSerializer
from projects.models import Project

class ProjectMessView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        # Lấy project và kiểm tra quyền truy cập
        project = Project.objects.filter(pk=project_id).first()
        if not project or (request.user != project.owner and request.user not in project.members.all()):
            return Response({'error': 'Bạn không có quyền truy cập vào project này.'}, status=status.HTTP_403_FORBIDDEN)

        # Lấy danh sách tin nhắn trong project
        messages = Mess.objects.filter(project=project).order_by('timestamp')
        serializer = MessSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        # Lấy project và kiểm tra quyền truy cập
        project = Project.objects.filter(pk=project_id).first()
        if not project or (request.user != project.owner and request.user not in project.members.all()):
            return Response({'error': 'Bạn không có quyền truy cập vào project này.'}, status=status.HTTP_403_FORBIDDEN)

        # Gửi tin nhắn trong project
        data = request.data.copy()
        data['project'] = project.id
        data['sender'] = request.user.id  # Gán sender là người dùng hiện tại

        serializer = MessSerializer(data=data)
        if serializer.is_valid():
            serializer.save(sender=request.user)  # Truyền sender vào phương thức save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)