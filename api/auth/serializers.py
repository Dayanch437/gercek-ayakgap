from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email","phone_number","password"]
        extra_kwargs = {"password": {"write_only": True},"username": {"required": False}}


    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', '')
        )

        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user