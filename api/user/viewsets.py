
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

User = get_user_model()
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.user.serializers import UserSerializer


@extend_schema(
    tags=['user'],
    description="",
    responses=UserSerializer
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.users.models import PasswordResetOTP

from .serializers import (RequestResetSerializer, ResetPasswordSerializer,
                          VerifyOTPSerializer)

User = get_user_model()

@extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {'type': 'string', 'format': 'email'},
            },
            'required': ['email'],
            'example': {
                'email': 'user@example.com'
            }
        }
    },
    responses={
        200: {
            'description': 'OTP sent successfully',
            'examples': {
                'application/json': {
                    'message': 'Verification code sent to your email'
                }
            }
        },
        400: {
            'description': 'Invalid request',
            'examples': {
                'application/json': {
                    'error': 'Invalid email format'
                }
            }
        },
        404: {
            'description': 'User not found',
            'examples': {
                'application/json': {
                    'error': 'No user with this email address'
                }
            }
        }
    },
    methods=['POST'],
    description='Request a password reset OTP to be sent to your email'
)
@api_view(['POST'])
@permission_classes([AllowAny])  # <--- This removes auth requirement
def request_password_reset(request):
    serializer = RequestResetSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "No user with this email address"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Generate and save OTP
    otp_obj = PasswordResetOTP.generate_otp(user)

    # Send email with OTP
    send_mail(
        'Your Password Reset OTP',
        f'Your verification code is: {otp_obj.otp}\n\nThis code will expire in 15 minutes.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    return Response(
        {"message": "Verification code sent to your email"},
        status=status.HTTP_200_OK
    )

@extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {'type': 'string', 'format': 'email'},
                'otp': {'type': 'string', 'maxLength': 6},
            },
            'required': ['email', 'otp'],
            'example': {
                'email': 'user@example.com',
                'otp': '123456'
            }
        }
    },
    responses={
        200: {
            'description': 'OTP verified',
            'examples': {
                'application/json': {
                    'message': 'OTP verified successfully'
                }
            }
        },
        400: {
            'description': 'Invalid OTP',
            'examples': {
                'application/json': [
                    {
                        'error': 'Invalid OTP or email'
                    },
                    {
                        'error': 'OTP expired or already used'
                    }
                ]
            }
        }
    },
    methods=['POST'],
    description='Verify the OTP received via email'
)
@api_view(['POST'])
@permission_classes([AllowAny])  # <--- This removes auth requirement
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    otp = serializer.validated_data['otp']

    try:
        user = User.objects.get(email=email)
        otp_obj = PasswordResetOTP.objects.filter(
            user=user,
            otp=otp,
            is_used=False
        ).latest('created_at')
    except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
        return Response(
            {"error": "Invalid OTP or email"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not otp_obj.is_valid():
        return Response(
            {"error": "OTP expired or already used"},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {"message": "OTP verified successfully"},
        status=status.HTTP_200_OK
    )



@extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {'type': 'string', 'format': 'email'},
                'otp': {'type': 'string', 'maxLength': 6},
                'new_password': {'type': 'string', 'format': 'password'},
                'confirm_password': {'type': 'string', 'format': 'password'},
            },
            'required': ['email', 'otp', 'new_password', 'confirm_password'],
            'example': {
                'email': 'user@example.com',
                'otp': '123456',
                'new_password': 'NewSecurePassword123!',
                'confirm_password': 'NewSecurePassword123!'
            }
        }
    },
    responses={
        200: {
            'description': 'Password reset successful',
            'examples': {
                'application/json': {
                    'message': 'Password reset successfully'
                }
            }
        },
        400: {
            'description': 'Validation error',
            'examples': {
                'application/json': [
                    {
                        'error': 'Passwords do not match'
                    },
                    {
                        'error': 'OTP verification failed'
                    }
                ]
            }
        }
    },
    methods=['POST'],
    description='Reset password after OTP verification'
)
@api_view(['POST'])
@permission_classes([AllowAny])  # <--- This removes auth requirement
def reset_password_with_otp(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    otp = serializer.validated_data['otp']
    new_password = serializer.validated_data['new_password']

    try:
        user = User.objects.get(email=email)
        otp_obj = PasswordResetOTP.objects.filter(
            user=user,
            otp=otp,
            is_used=False
        ).latest('created_at')
    except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
        return Response(
            {"error": "Invalid OTP or email"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not otp_obj.is_valid():
        return Response(
            {"error": "OTP expired or already used"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(new_password)
    user.save()

    # Mark OTP as used
    otp_obj.is_used = True
    otp_obj.save()

    return Response(
        {"message": "Password reset successfully"},
        status=status.HTTP_200_OK
    )

# class ProfileView(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = ProfileSerializer
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         qs = qs.filter(email=self.request.user.email)
#         return qs
