import uuid

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer


# Task
class TaskListCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(userId=request.user).order_by('-createdAt')

        # Lấy các query param nếu có
        status_param = request.query_params.get('status')
        priority_param = request.query_params.get('priority')
        due_date_param = request.query_params.get('due_date')  # định dạng: YYYY-MM-DD

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
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(userId=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            # Convert bất kể có gạch hay không
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
        
        task = get_object_or_404(Task, id=pk, userId=request.user)
        # Cập nhật công việc với dữ liệu từ request, cho phép cập nhật một phần
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

# End Task
