from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.auth.serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()  # Always use this for custom user model


class UserCreateView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = self.get_tokens_for_user(user)

        return Response(
            {
                "user": serializer.data,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
