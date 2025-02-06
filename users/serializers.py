from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from users.middleware import get_current_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
        read_only_fields = ('is_staff', 'is_active')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class AbstractCreatorUserSerializerMixin(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    
    def create(self, validated_data):
        validated_data['created_by'] = get_current_user()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = get_current_user()
        return super().update(instance, validated_data)