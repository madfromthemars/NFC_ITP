# Rest
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

# Django
from django.contrib import auth

# Local
from main.models import User

class getContact_Serializer(serializers.Serializer):
    nick_name = serializers.CharField(required=True, max_length=255, source='username')
    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)

    birthday = serializers.DateField(allow_null=True, )

    phone = serializers.CharField(required=True, max_length=255)
    email = serializers.EmailField(required=True, max_length=255)

    work_info = serializers.JSONField(allow_null=True)
    address = serializers.JSONField(allow_null=True)


class Login_Serializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=16, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()
    @staticmethod
    def get_tokens(obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact Admin')
        return {'tokens': user.tokens, 'username': username}


class ChangePassword_Serializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=16, min_length=6)
    new_password = serializers.CharField(max_length=16, min_length=6)
    new_password_dup = serializers.CharField(max_length=16, min_length=6)



