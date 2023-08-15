from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Local
from .models import User, Order


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    address = serializers.DictField(allow_null=True, allow_empty=True)
    work_info = serializers.DictField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password',
                  'first_name', 'last_name', 'birthday',
                  'phone', 'work_info', 'address', 'type', 'theme']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'birthday': {'required': False},
            'phone': {'required': False},
            'work_info': {'required': False},
            'address': {'required': False},
            'type': {'required': False},
            'theme': {'required': False}
        }

    def validate(self, attrs):
        username = attrs.get('username', '')
        user_type = attrs.get('type', '')
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        if user_type not in ("REGULAR", "COMPANY") and user_type:
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    @staticmethod
    def get_tokens(obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['password', 'username', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact Admin')
        return {'tokens': user.tokens, 'username': username}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refreshToken = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.refreshToken).blacklist()
        except TokenError:
            raise TokenError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(write_only=True, required=False)
    type = serializers.CharField(default="REGULAR", read_only=True)

    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)
    birthday = serializers.DateField(allow_null=True, )

    phone = serializers.CharField(required=True, max_length=255)
    email = serializers.EmailField(required=True, max_length=255)

    work_info = serializers.JSONField(allow_null=True)
    address = serializers.JSONField(allow_null=True)

    created_by_id = serializers.IntegerField(default=None, allow_null=True)
    theme = serializers.CharField(max_length=255, required=False, allow_null=True, default=None)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'type', 'first_name', 'last_name', 'birthday',
            'phone', 'email', 'work_info', 'address', 'created_by_id', 'password',
            'theme'
        )

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        created_by_id = validated_data.pop('created_by_id')
        user = User.objects.create_user(username=username, password=password, created_by_id=created_by_id,
                                        **validated_data)
        return user


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(required=True)
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    status = serializers.CharField(default="NEW")

    class Meta:
        model = Order
        fields = ('id', 'user_id', 'status', 'updated_at', 'created_at')

