from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('username', 'password', 'email', 'first_name', 'last_name')
        }),
        ('Thông tin cá nhân', {
            'fields': ('phone_number', 'address', 'date_of_birth', 'profile_picture')
        }),
        ('Quyền hạn', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')
        }),
        ('Thông tin đăng nhập', {
            'fields': ('last_login', 'date_joined')
        }),
    ) 