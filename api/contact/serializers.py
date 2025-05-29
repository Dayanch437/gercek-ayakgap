from random import randint
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import serializers
from datetime import datetime


class ContactSerializer(serializers.Serializer):
    username = serializers.CharField()
    gmail = serializers.EmailField()
    comment = serializers.CharField()

    def save(self):
        verification_code = str(randint(100000, 999999))
        print(verification_code)
        gmail = self.validated_data['gmail']

        # Cache the verification data
        cache.set(
            f'verification_{gmail}',
            {
                'code': verification_code,
                'username': self.validated_data['username'],
                'comment': self.validated_data['comment'],
            },
            timeout=600,  # Cache timeout in seconds
        )
        code = verification_code
        current_time = datetime.now().year
        html_content = render_to_string(
            "emails/user_verification.html",
            {
                "code": code,
                "current_year": current_time,
            }
        )



        send_mail(
            'Email Verification Code',
            f'Your verification code is: {verification_code}',
            settings.DEFAULT_FROM_EMAIL,
            (gmail,),
            html_message=html_content,
            fail_silently=False,
        )


class ContactVerificationSerializer(serializers.Serializer):
    gmail = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)
