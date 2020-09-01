from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import create_event

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = UserModel
        fields = ["username", "first_name", "last_name", "email", "password"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = create_event
        fields = '__all__'