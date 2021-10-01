from djoser.serializers import UserCreateSerializer, SendEmailResetSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()
from .models import NewUsers


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = NewUsers
        fields = ('id', 'email', 'password')


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profilePic', 'is_superuser']