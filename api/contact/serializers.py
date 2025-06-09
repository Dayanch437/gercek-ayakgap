from rest_framework import serializers
from apps.adds.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'user',
            'id',
            'gmail',
            'phone',
            'comment'
        ]
        extra_kwargs = {
            'user': {'required': False      },
        }

    def create(self, validated_data):
        user = self.context['request'].user
        return Contact.objects.create(user=user, **validated_data)
