# Rest
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

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


class Logout_Serializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refreshToken = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.refreshToken).blacklist()
        except TokenError:
            raise TokenError


class ChangePassword_Serializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=16)
    new_password = serializers.CharField(max_length=16, min_length=8)
    new_password_dup = serializers.CharField(max_length=16, min_length=8)


class Register_Serializer(serializers.Serializer):
    # Names
    first_name = serializers.CharField(max_length=255, required=True)
    middle_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=True)

    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=16, min_length=8, required=True)
    password_dup = serializers.CharField(max_length=16, min_length=8, required=True)

    # Email
    email = serializers.EmailField(required=True)
    work_email = serializers.EmailField(required=False)

    # Phones
    home_phone = serializers.CharField(max_length=255, required=False)
    work_phone = serializers.CharField(max_length=255, required=False)
    cell_phone = serializers.CharField(max_length=255, required=False)

    # Work
    organization = serializers.CharField(max_length=255, required=False)
    title = serializers.CharField(max_length=255, required=False)
    role = serializers.CharField(max_length=255, required=False)
    work_url = serializers.URLField(required=False)

    # Work Address
    work_street = serializers.CharField(max_length=255, required=False)
    work_city = serializers.CharField(max_length=255, required=False)
    work_state_or_province = serializers.CharField(max_length=255, required=False)
    work_postal_code = serializers.CharField(max_length=255, required=False)
    work_country = serializers.CharField(max_length=255, required=False)

    # Address
    street = serializers.CharField(max_length=255, required=False)
    region = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255, required=False)
    state_or_province = serializers.CharField(max_length=255, required=False)
    postal_code = serializers.CharField(max_length=255, required=False)
    country = serializers.CharField(max_length=255, required=False)

    # Personal
    birthday = serializers.DateField(required=False)
        # TODO -> Move it to User get it from user itself
    GENDER_CHOICES = (
        ('M', "Male"),
        ('F', 'Female'),
    )
    gender = serializers.ChoiceField(GENDER_CHOICES, required=False)

    # Image
    photo = serializers.ImageField(required=False)

    # Social URL
    linkedin = serializers.URLField(required=False)
    twitter = serializers.URLField(required=False)
    facebook = serializers.URLField(required=False)
    instagram = serializers.URLField(required=False)
    telegram = serializers.URLField(required=False)
    youtube = serializers.URLField(required=False)
    custom = serializers.URLField(required=False)

