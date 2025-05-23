from rest_framework import permissions, status
# 🚪 Logout (JWT: blacklist refresh token)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import CustomTokenObtainPairSerializer, UserSerializer


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request):
        if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']):
            return Response({'error': 'Chỉ admin hoặc manager được phép truy cập.'}, status=status.HTTP_403_FORBIDDEN)
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
                'data':{
                    'id': user.id,
                    'username': user.username,
                    'role': user.role if hasattr(user, 'role') else None,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email hoặc mật khẩu không đúng.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    print(APIView)
    permission_classes = [IsAuthenticated]
    print(permission_classes)
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Thiếu Authorization header'}, status=400)

        refresh_token = auth_header.split(' ')[1]
        print(refresh_token)

        try:
            # Kiểm tra token loại Refresh
            token = RefreshToken(refresh_token)
            # Chỉ blacklist refresh token
            token.blacklist()
            return Response({'message': 'Đăng xuất thành công.'}, status=205)
        except TokenError as e:
            return Response({'error': f'Token không hợp lệ hoặc đã hết hạn: {str(e)}'}, status=400)
