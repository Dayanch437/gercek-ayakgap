import random
from datetime import timedelta
from apps.utils.fields import CompressedImageField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, first_name="", last_name="", phone_number=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")

        if self.model.objects.filter(username=username).exists():
            raise ValueError("Superuser creation failed: Username already exists.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.set_password(password)
        user.save(using=self._db)
        return user



class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    avatar = CompressedImageField(upload_to="avatar", null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.email if self.email else self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


    @classmethod
    def generate_otp(cls, user):
        # Delete any existing OTPs for this user
        cls.objects.filter(user=user).delete()
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        return cls.objects.create(user=user, otp=otp)
    def is_valid(self):
        return not self.is_used and (timezone.now() - self.created_at) < timedelta(minutes=15)