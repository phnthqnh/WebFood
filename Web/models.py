from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone

class UserAccountManager(BaseUserManager):
    # Tạo người dùng thông thường
    def create_user(self, username, email, password=None, role='customer', **extra_fields):
        if not email:
            raise ValueError('Người dùng phải có một địa chỉ email')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Mã hóa mật khẩu
         # Đặt is_staff dựa trên role
        if role in ['staff', 'manager']:
            user.is_staff = True
        else:
            user.is_staff = False
        user.save(using=self._db)
        return user

    # Tạo người dùng quản trị
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'manager')
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, role='manager', **extra_fields)
    
     # Tùy chỉnh hàm authenticate
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserAccount = get_user_model()  # Lấy mô hình người dùng hiện tại
        try:
            user = UserAccount.objects.get(email=email)  # Sử dụng User.objects thay vì self.get_queryset()
        except UserAccount.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

# Bảng cha: User
class User(AbstractBaseUser, PermissionsMixin):  # AbstractUser đã tích hợp username, password, email
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='manager')
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Chỉ định quyền truy cập Admin
    is_superuser = models.BooleanField(default=False)  # Quyền quản trị cao nhất

    # Trường mà Django sẽ sử dụng để xác định danh tính người dùng
    USERNAME_FIELD = 'email'  # Bạn có thể chọn 'email' nếu muốn đăng nhập bằng email
    REQUIRED_FIELDS = ['username']  # Những trường bắt buộc khi tạo superuser
    
     # Thêm trường date_joined
    date_joined = models.DateTimeField(default=timezone.now)

    # Trình quản lý cho mô hình này
    objects = UserAccountManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        
    def save(self, *args, **kwargs):
        # tao role tu dong khi tao moi project
        if self.role in ['staff', 'manager']:
            self.is_staff = True
        else:
            self.is_staff = False
        super(User, self).save(*args, **kwargs)
        r = self.role
        # print(r)
        if (r == 'staff'):
            try:
                stf = Staff.objects.get(user = self)
                # user = User.objects.get(email = self.email)
                # # user.is_active = True
                # user.save()
            except:
                stf = Staff.objects.create(user = self)
                stf.save()
        elif (r == 'manager'):
            try:
                manager = Manager.objects.get(user = self)
            except:
                manager = Manager.objects.create(user = self)
                manager.save()
        else:
            # raise ValidationError("Không thể tạo mới khách hàng!")
            try:
                cus = Customer.objects.get(user = self)
            except:
                cus = Customer.objects.create(user = self)
                cus.save()
            # if r == 'customer': continue
            # try:
            #     role= Role.objects.get(project= self, role= r)
            # except:
            #     role= Role(project= self, role= r)
            #     role.save()

# Bảng con: Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer_profile')


    class Meta:
        db_table = "customer"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

# Bảng con: Staff
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff_profile')
    # department = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "staff"
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"

# Bảng con: Manager
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='manager_profile')
    # team_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "manager"
        verbose_name = "Manager"
        verbose_name_plural = "Managers"
        
# Bảng Category
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name


# Bảng product
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.URLField()
    price = models.IntegerField()
    description = models.TextField(blank=True)
    STATUS_CHOICES = [
        ('còn hàng', 'còn hàng'),
        ('tạm ngưng', 'tạm ngưng'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='còn hàng')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.FloatField(null=True, default=0.0, blank=True)
    sold = models.IntegerField(null=True, default=10, blank=True)
    
    def __str__(self):
        return self.name
