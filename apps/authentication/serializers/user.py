"""User serializers for authentication"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.core.serializers.base import BaseModelSerializer
from apps.authentication.security import is_password_strong

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match"})
        is_strong, errors = is_password_strong(data['password'])
        if not is_strong:
            raise serializers.ValidationError({"password": errors})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserResponseSerializer(BaseModelSerializer):
    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                  'is_student', 'is_faculty', 'is_parent', 'is_active', 'roles',
                  'created_at', 'updated_at', 'last_login']
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']
    
    def get_roles(self, obj):
        user_roles = obj.user_roles.select_related('role').filter(role__is_active=True)
        return [ur.role.name for ur in user_roles]

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
    
    def validate_email(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value
