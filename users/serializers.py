from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 🧩 Thêm thông tin tùy chỉnh vào token
        token["id"] = str(user.id)
        token["username"] = user.username
        token["role"] = getattr(user, 'role', None)
        token["is_active"] = user.is_active
        token["is_staff"] = user.is_staff

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # 📤 Thêm các thông tin user vào response (ngoài token)
        data['message'] = 'Đăng nhập thành công.'
        data['id'] = str(user.id)
        data['username'] = user.username
        data['role'] = getattr(user, 'role', None)
        data['is_active'] = user.is_active
        data['is_staff'] = user.is_staff

        return data