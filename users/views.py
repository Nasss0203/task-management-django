# users/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .serializers import UserSerializer


class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # hoặc bỏ nếu cho public

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# 🆕 Create user (register)
class UserCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔐 Login
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email và mật khẩu là bắt buộc.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Email hoặc mật khẩu không đúng.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'Tài khoản đã bị vô hiệu hóa.'}, status=status.HTTP_403_FORBIDDEN)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Đăng nhập thành công.',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email hoặc mật khẩu không đúng.'}, status=status.HTTP_401_UNAUTHORIZED)


# 🚪 Logout (JWT: blacklist refresh token)

class UserLogoutView(APIView):
    permission_classes = [AllowAny]  # ✅ Cho phép tất cả gọi logout

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error': 'Thiếu refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Đăng xuất thành công.'}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({'error': 'Token không hợp lệ hoặc đã hết hạn.'}, status=status.HTTP_400_BAD_REQUEST)