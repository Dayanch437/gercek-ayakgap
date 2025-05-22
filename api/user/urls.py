from rest_framework.routers import DefaultRouter
from django.urls import path
from api.user.viewsets import UserViewSet,ProfileView
from .viewsets import (
request_password_reset,
    verify_otp,
    reset_password_with_otp
)


router = DefaultRouter()
router.register('user', UserViewSet)
router.register('profile', ProfileView,basename='profile')

urlpatterns = [
    path('request-reset/', request_password_reset, name='request-password-reset'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('reset-password/', reset_password_with_otp, name='reset-password'),
]
urlpatterns += router.urls