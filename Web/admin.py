from django.contrib import admin
from Web.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from typing import Any
from django.contrib import admin
from django.conf import settings

class UserAdmin(BaseUserAdmin):
    # Các trường hiển thị trong danh sách quản lý
    list_display = ['username', 'role', 'email', 'is_staff', 'is_active', 'is_superuser']
    list_filter = ['role', 'is_active', 'is_staff']

    # Các trường có thể tìm kiếm trong bảng User
    search_fields = ['username', 'email']

    # Các trường cần hiển thị trong form thêm/sửa người dùng
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Personal info', {'fields': ('phone_number', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'role', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # # Cấu hình phân quyền
    # filter_horizontal = ('groups', 'user_permissions',)
    
    def not_allow_edit(modeladmin, request, queryset):
        settings.ALLOW_EDIT_BY_ADMIN_ONLY = True
    def allow_edit(modeladmin, request, queryset):
        settings.ALLOW_EDIT_BY_ADMIN_ONLY = False
    not_allow_edit.short_description = "Not Allow Edit"
    allow_edit.short_description = 'Allow Edit'
    actions = [not_allow_edit, allow_edit]
    def get_action(self, action):
        return super().get_action(action)
    def get_list_editable(self, request):
        if settings.ALLOW_EDIT_BY_ADMIN_ONLY and not request.user.is_superuser:
            return None
        return super().get_list_editable(request)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly_fields += ['is_active', 'is_staff', 'is_superuser', 'role', 'last_login', 'date_joined']
        return readonly_fields
        
    def has_view_permission(self, request, obj=None):
        if request.user.is_staff:
            return True

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.id == request.user.id and obj.role in ['employee', 'manager']:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_module_permission(self, request):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False

# Đăng ký model `User` với Django Admin
admin.site.register(User, UserAdmin)

# Đăng ký các model con `Customer`, `Employee`, `Manager`
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Manager)

admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'status_view']
    list_filter = ['status', 'category']
    search_fields = ('name', 'status')
    def not_allow_edit(modeladmin, request, queryset):
        settings.ALLOW_EDIT_BY_ADMIN_ONLY = True
    def allow_edit(modeladmin, request, queryset):
        settings.ALLOW_EDIT_BY_ADMIN_ONLY = False
    not_allow_edit.short_description = "Not Allow Edit"
    allow_edit.short_description = 'Allow Edit'
    actions = [not_allow_edit, allow_edit]
    def get_action(self, action):
        return super().get_action(action)
    def get_list_editable(self, request):
        if settings.ALLOW_EDIT_BY_ADMIN_ONLY and not request.user.is_superuser:
            return None
        return super().get_list_editable(request)

    # def get_readonly_fields(self, request, obj=None):
    #     # readonly_fields = super().get_readonly_fields(request, obj)
    #     # if settings.ALLOW_EDIT_BY_ADMIN_ONLY and not request.user.is_superuser:
    #     #     return readonly_fields + [field.author for field in self.model._meta.fields]
    #     # return readonly_fields
        
    #     if request.user.is_staff or request.user.is_superuser:
    #         readonly_fields = list(super().get_readonly_fields(request, obj))
    #         return readonly_fields + ['author', 'liked_by']
    #     return super().get_readonly_fields(request, obj)
        
    def has_view_permission(self, request, obj=None):
        if request.user.is_staff:
            return True

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

    def has_module_permission(self, request):
        if request.user.is_staff:
            return True
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'customer', 'employee', 'tongtien', 'status_view']
    list_filter = ['status', 'employee']
    search_fields = ['order__tracking_number', 'customer']
    autocomplete_fields=('products',)
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'total_value']
    list_filter = ['order__tracking_number']
    search_fields = ['order__tracking_number']
admin.site.register(OrderItem, OrderItemAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'quantity', 'total_value']
    list_filter = ['customer']
    autocomplete_fields=('products',)
admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'price']
    list_filter = ['cart']
admin.site.register(CartItem, CartItemAdmin)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discountvalue', 'minimum']
admin.site.register(Discount, DiscountAdmin)

admin.site.register(PaymentMethod)
admin.site.register(BusinessInfo)