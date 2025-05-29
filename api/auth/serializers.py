from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()  # Always use this for custom user models


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email","phone_number","password"]
    def create(self, validated_data):
        return User.objects.create(**validated_data)