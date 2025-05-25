import uuid

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.permissions import IsTaskOwnerOrReadOnly
from tasks.models import Task, Assignment
from tasks.serializers import TaskSerializer
from projects.models import Project 
from users.models import User

# Task
class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(userId=request.user).order_by('-createdAt')

        # Lấy các query param nếu có
        status_param = request.query_params.get('status')
        priority_param = request.query_params.get('priority')
        due_date_param = request.query_params.get('due_date')

        if status_param:
            tasks = tasks.filter(status=status_param)

        if priority_param:
            tasks = tasks.filter(priority=priority_param)

        if due_date_param:
            tasks = tasks.filter(dueDate=due_date_param)

        if not tasks.exists():
            return Response({"detail": "No tasks found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


    def post(self, request):
            project_id = request.data.get('projectId')
            if project_id:
                project = get_object_or_404(Project, pk=project_id)
                # Nếu là project nhóm thì chỉ admin/manager mới được tạo
                if not project.is_personal:
                    if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']):
                        return Response({'error': 'Chỉ admin hoặc manager được tạo task trong project nhóm.'}, status=403)
            # Nếu không có project hoặc project cá nhân: ai cũng tạo được
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(userId=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated, IsTaskOwnerOrReadOnly]

    def get(self, request, pk):
        try:
            
            pk = uuid.UUID(pk)
        except ValueError:
            return Response({"detail": "Invalid UUID format."}, status=400)

        task = get_object_or_404(Task, id=pk, userId=request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

class UpdateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            pk = uuid.UUID(pk)
        except ValueError:
            return Response({"detail": "Invalid UUID format."}, status=400)

        # Lấy task
        task = get_object_or_404(Task, id=pk)

        # Kiểm tra quyền truy cập
        if task.projectId:  # Nếu task thuộc về một project
            if request.user != task.userId and request.user not in task.projectId.members.all():
                if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']):
                    return Response({'error': 'Bạn không có quyền cập nhật task này.'}, status=status.HTTP_403_FORBIDDEN)
        else:  # Nếu task không thuộc project nào
            if request.user != task.userId:
                return Response({'error': 'Bạn không có quyền cập nhật task này.'}, status=status.HTTP_403_FORBIDDEN)

        # Cập nhật task
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        # Lấy công việc cần xóa
        try:
            # Convert bất kể có gạch hay không
            pk = uuid.UUID(pk)
        except ValueError:
            return Response({"detail": "Invalid UUID format."}, status=400)
        task = get_object_or_404(Task, id=pk, userId=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Lấy danh sách công việc của một project
class ProjectTaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        if request.user != project.owner and request.user not in project.members.all():
            if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']):
                return Response({'error': 'Bạn không có quyền truy cập project này.'}, status=status.HTTP_403_FORBIDDEN)

        tasks = Task.objects.filter(projectId=project)

        status_param = request.query_params.get('status')
        if status_param:
            tasks = tasks.filter(status=status_param)

        if not tasks.exists():
            return Response({"detail": "No tasks found for this project."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
# End Tasks
