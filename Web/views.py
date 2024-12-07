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


# Danh sách sản phẩm
@api_view(['GET'])
def get_products(request):
    try: 
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Không tìm thấy sản phẩm.'}, status=status.HTTP_404_NOT_FOUND)


# Tạo mới sản phẩm
@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Sửa sản phẩm
@api_view(['PUT'])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Sản phẩm không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Xóa sản phẩm
@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'message': 'Sản phẩm đã được xóa thành công.'}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'error': 'Sản phẩm không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

# Danh sách Category
@api_view(['GET'])
def get_categories(request):
    try: 
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({'error': 'Không tìm thấy danh mục.'}, status=status.HTTP_404_NOT_FOUND)

# Tạo mới Category
@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Sửa Category
@api_view(['PUT'])
def update_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Danh mục không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Xóa Category
@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response({'message': 'Danh mục đã được xóa thành công.'}, status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({'error': 'Danh mục không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
    