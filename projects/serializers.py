from rest_framework import serializers

from tasks.serializers import TaskSerializer
from .models import Project
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Project
        fields = '__all__'


    # Lấy danh sách task trong project
    def get_tasks(self, obj):
        tasks = obj.tasks.all()
        return TaskSerializer(tasks, many=True, context=self.context).data