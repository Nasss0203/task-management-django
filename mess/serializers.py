from rest_framework import serializers
from .models import Mess

class MessSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Mess
        fields = ['id', 'project', 'project_name', 'sender', 'receiver', 'sender_username', 'receiver_username', 'content', 'timestamp', 'is_read']
        read_only_fields = ['id', 'timestamp', 'sender', 'sender_username', 'receiver_username', 'project_name']