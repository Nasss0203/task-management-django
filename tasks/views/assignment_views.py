import uuid

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.models import Task, Assignment
from projects.models import Project 
from users.models import User
from tasks.serializers import UserSerializer, TaskSerializer


# Assignments
class AssignTaskView(APIView):
    def post(self, request):
        task_id = request.data.get('task_id')
        user_id = request.data.get('user_id')

        # Kiểm tra task
        task = get_object_or_404(Task, pk=task_id)

        # Kiểm tra user
        user = get_object_or_404(User, pk=user_id)

        # Kiểm tra quyền
        if not task.projectId.is_personal and not (hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']):
            return Response({'error': 'Chỉ admin hoặc manager được phân task trong project nhóm.'}, status=403)

        # Tạo assignment
        assignment, created = Assignment.objects.get_or_create(task=task, user=user)
        if not created:
            return Response({'error': 'Task đã được phân cho user này.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': f'Task đã được phân cho {user.username}.'}, status=status.HTTP_201_CREATED)
    

class AssignmentListByTaskView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        assignments = Assignment.objects.filter(task=task)
        users = [assignment.user for assignment in assignments]

        user_serializer = UserSerializer(users, many=True)
        return Response({
            "task_id": str(task.id),
            "assigned_users": user_serializer.data
        })

class UserAssignmentsView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        assignments = Assignment.objects.filter(user=user)
        tasks = [assignment.task for assignment in assignments]

        task_serializer = TaskSerializer(tasks, many=True)
        return Response({
            "user_id": str(user.id),
            "assigned_tasks": task_serializer.data
        })
    
class DeleteAssignmentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        task_id = request.data.get('task_id')
        user_id = request.data.get('user_id')

        if not task_id or not user_id:
            return Response(
                {"error": "Cần cung cấp cả task_id và user_id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kiểm tra assignment
        assignment = Assignment.objects.filter(task_id=task_id, user_id=user_id).first()
        if not assignment:
            return Response(
                {"error": "Không tìm thấy assignment phù hợp."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Kiểm tra quyền
        task = assignment.task
        if task.projectId and not task.projectId.is_personal:
            # Nếu là project nhóm, chỉ admin hoặc manager được phép xóa
            if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']):
                return Response(
                    {"error": "Chỉ admin hoặc manager được phép xóa assignment trong project nhóm."},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif task.projectId and task.projectId.is_personal:
            # Nếu là project cá nhân, chỉ owner được phép xóa
            if task.projectId.owner != request.user:
                return Response(
                    {"error": "Chỉ owner được phép xóa assignment trong project cá nhân."},
                    status=status.HTTP_403_FORBIDDEN
                )

        
        assignment.delete()
        return Response(
            {"message": "Xóa assignment thành công."},
            status=status.HTTP_200_OK
        )