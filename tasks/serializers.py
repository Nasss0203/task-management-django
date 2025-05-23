from rest_framework import serializers
from .models import Task, Assignment
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.SerializerMethodField() 

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'createdAt', 'updatedAt', 'userId']

    def get_assigned_users(self, obj):
        assignments = Assignment.objects.filter(task=obj)
        return UserSerializer([assignment.user for assignment in assignments], many=True).data