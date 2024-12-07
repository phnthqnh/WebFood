from rest_framework import serializers
from Web.models import *

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email và mật khẩu là bắt buộc.')

        # Không cần tạo đối tượng User ở đây
        return data  # Trả về dữ liệu đã xác thực
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    # def validate(self, data):
    #     # Đảm bảo rằng người đăng ký chỉ được phép là customer
    #     if 'role' in data and data['role'] != 'customer':
    #         raise serializers.ValidationError("Chỉ khách hàng được phép đăng ký tài khoản.")
    #     return data

    def create(self, validated_data):
        # Tạo người dùng mới với vai trò mặc định là 'customer'
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        user.role = 'customer'  # Gán vai trò mặc định
        user.save()
        return user
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'