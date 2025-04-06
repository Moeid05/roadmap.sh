from rest_framework import serializers
from .models import CustomUser

from django.contrib.auth import get_user_model
User  = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
