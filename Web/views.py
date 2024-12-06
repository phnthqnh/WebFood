from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *

@api_view(['POST'])
def login(request):
    """
    Đăng nhập người dùng, trả về JWT Token nếu xác thực thành công.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Xác thực người dùng
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and user.role == 'customer':
                # Tạo token nếu mật khẩu đúng
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'userID': user.id,
                    'email': user.email,
                    'username': user.username,
                    'role': user.role,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Mật khẩu không chính xác.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Người dùng không tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    """
    Đăng ký tài khoản cho khách hàng.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Đăng ký thành công!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)