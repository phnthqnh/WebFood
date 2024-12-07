from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.html import format_html
import random
import string

class UserAccountManager(BaseUserManager):
    # Tạo người dùng thông thường
    def create_user(self, username, email, password=None, role='customer', **extra_fields):
        if not email:
            raise ValueError('Người dùng phải có một địa chỉ email')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Mã hóa mật khẩu
         # Đặt is_staff dựa trên role
        if role in ['employee', 'manager']:
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
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='manager')
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
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
        
    def __str__(self):
        return self.username
        
    def save(self, *args, **kwargs):
        # tao role tu dong khi tao moi project
        if self.role in ['employee', 'manager']:
            self.is_staff = True
        else:
            self.is_staff = False
        super(User, self).save(*args, **kwargs)
        r = self.role
        # print(r)
        if (r == 'employee'):
            try:
                stf = Employee.objects.get(user = self)
                # user = User.objects.get(email = self.email)
                # # user.is_active = True
                # user.save()
            except:
                stf = Employee.objects.create(user = self)
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
        
    def __str__(self):
        return self.user.username

# Bảng con: Employee
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='semployee_profile')
    # department = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "employee"
        verbose_name = "employee"
        verbose_name_plural = "employee"
        
    def __str__(self):
        return self.user.username

# Bảng con: Manager
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='manager_profile')
    # team_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "manager"
        verbose_name = "Manager"
        verbose_name_plural = "Managers"
    
    def __str__(self):
        return self.user.username
        
# Bảng Category
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


# Bảng product
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.URLField()
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
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
    
    def status_view(self):
        try:
            if self.status == 'tạm ngưng':
                status_color= '#FF0000'
                status = self.status
            else:
                status_color= '#000000'
                status = self.status

            html= f'<span style="color: {status_color};">{status}</span>'
            return format_html(html)
        except:
            return 0
    status_view.short_description = 'Trạng thái'
    
    
class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(null=True, blank=True)
    discountvalue = models.PositiveSmallIntegerField()
    minimum = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return str(self.discountvalue) + '%'
    
class PaymentMethod(models.Model):
    id = models.AutoField(primary_key=True)
    METHOD_CHOICES = [
        ('COD', 'COD'),
        ('MOMO', 'MOMO'),
    ]
    methodname = models.CharField(max_length=20, choices=METHOD_CHOICES, default='COD')
    QRcode = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.methodname


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    STATUS_CHOICES = [
        # "Chờ xác nhận", "Đang chuẩn bị",  "Đang giao", "Hoàn thành" và"Hủy"
        ("Chờ xác nhận", 'Chờ xác nhận'),  # Trạng thái mặc định
        ("Đang chuẩn bị", 'Đang chuẩn bị'),
        ("Đang giao", 'Đang giao'),
        ("Hoàn thành", 'Hoàn thành'),
        ("Hủy", 'Hủy'),
    ]

    tracking_number = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Chờ xác nhận')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hovaten = models.CharField(max_length=200, null=True, blank=True)
    sdt = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    diachi = models.CharField(max_length=255, null=True, blank=True)
    tongtien = models.FloatField(default=0.0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Liên kết với người dùng
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) 
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, name="Payment Method")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.tracking_number
    
    def save(self, *args, **kwargs):
        self.hovaten = self.customer.user.username
        self.sdt = self.customer.user.phone_number
        self.email = self.customer.user.email
        self.diachi = self.customer.user.address
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        super().save(*args, **kwargs)

    def generate_tracking_number(self):
        return ''.join(random.choices(string.digits, k=10)) 
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    
    # def __str__(self):
    #     return self.order.tracking_number
    
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    total_value = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Cart of {self.customer.user.username}"
      
class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart}"
    
    # def total_products(self):

        
    
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)
        cartitem = CartItem.objects.filter(cart=self.cart)
        # print("cartitem: ", cartitem.count())
        cart = Cart.objects.get(id = self.cart.id)
        cart.total_value += self.price
        cart.quantity = cartitem.count()
        cart.save()
        
class BusinessInfo(models.Model):
    id = models.AutoField(primary_key=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    