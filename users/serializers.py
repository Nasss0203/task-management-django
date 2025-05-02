from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email này đã được sử dụng.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
