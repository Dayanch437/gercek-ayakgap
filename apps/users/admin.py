# admin.py

from django.contrib import admin
from .models import User, PasswordResetOTP

class PasswordResetOTPInline(admin.TabularInline):
    model = PasswordResetOTP
    extra = 0
    readonly_fields = ('otp', 'created_at', 'is_used')
    can_delete = False
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_superadmin', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'avatar')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superadmin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    inlines = [PasswordResetOTPInline]

admin.site.register(User, CustomUserAdmin)
