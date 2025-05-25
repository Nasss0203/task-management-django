from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .permissions import IsProjectOwnerOrManager
from tasks.serializers import TaskSerializer
from .models import Project
from .serializers import ProjectSerializer,UserSerializer
from users.models import User
from tasks.models import Task

class ProjectListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(owner=request.user).order_by('-createdAt')

        status_param = request.query_params.get('status')

        if status_param:
            projects = projects.filter(status=status_param)

        if not projects.exists():
            return Response({"detail": "No tasks found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        is_personal = request.data.get('is_personal', False)
        
        if not is_personal:
            if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']):
                return Response({'error': 'Chỉ admin hoặc manager được tạo project nhóm.'}, status=403)
       
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, is_personal=is_personal)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, owner=request.user)
        except Project.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class ProjectUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, owner=request.user)
            
        except Project.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        project = get_object_or_404(Project, pk=pk)
        if not project.is_personal:
            if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']):
                return Response({'error': 'Chỉ admin hoặc manager được thao tác với project nhóm.'}, status=403)
        else:
            if project.owner != request.user:
                return Response({'error': 'Chỉ owner được thao tác với project cá nhân.'}, status=403)
            
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, owner=request.user)
        except Project.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        Task.objects.filter(projectId=project).delete()
       
        project.members.clear()
      
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectAddMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "Missing user_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_to_add = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        project.members.add(user_to_add)
        project.save()

        return Response({"detail": f"User {user_id} added to project members."}, status=status.HTTP_200_OK)


class TaskCreateInProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id, owner=request.user)
        task_id = request.data.get('task_id')

        if not task_id:
            return Response({'error': 'task_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        task = get_object_or_404(Task, pk=task_id, userId=request.user)
        task.projectId = project  # Sửa dòng này
        task.save()

        return Response({'message': 'Task added to project successfully.'})
    

class RemoveMemberFromProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, project_id):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        project = get_object_or_404(Project, pk=project_id)
        try:
            user_to_remove = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        project.members.remove(user_to_remove)
        project.save()
        return Response({'message': 'Member removed from project.'}, status=status.HTTP_200_OK)
    

class RemoveTaskFromProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, project_id):
        task_id = request.data.get('task_id')
        if not task_id:
            return Response({'error': 'task_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        project = get_object_or_404(Project, pk=project_id)
        task = get_object_or_404(Task, pk=task_id, projectId=project)
        task.projectId = None
        task.save()
        return Response({'message': 'Task removed from project.'}, status=status.HTTP_200_OK)
    

# Fetch danh sách thành viên của project
class ProjectMembersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        if request.user not in project.members.all() and request.user != project.owner:
            return Response({'error': 'Bạn không có quyền truy cập vào project này.'}, status=403)

        members = project.members.all()

        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)

class ProjectTaskListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        if request.user not in project.members.all():
            return Response({'error': 'Bạn không thuộc project này.'}, status=status.HTTP_403_FORBIDDEN)

        tasks = Task.objects.filter(projectId=project)

        status_param = request.query_params.get('status')
        if status_param:
            tasks = tasks.filter(status=status_param)

        if not tasks.exists():
            return Response({"detail": "No tasks found for this project."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize danh sách task
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
# Lấy danh sách các project mà người dùng sở hữu hoặc là thành viên
class MyProjectsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        owned_projects = Project.objects.filter(owner=user)
        member_projects = Project.objects.filter(members=user).exclude(owner=user)

        projects = owned_projects | member_projects

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)