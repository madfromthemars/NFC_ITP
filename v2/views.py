# Django
from django.core.mail import send_mail

# Rest
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# 3rd Party
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Local
from .serializers import (
    getContact_Serializer, Login_Serializer, ChangePassword_Serializer, Register_Serializer,
    Logout_Serializer
)
from main.models import User
from .utils import generate_Password
from .permissions import ResetPasswordPermission
user = getContact_Serializer()

@swagger_auto_schema(
    methods=['GET'],
    responses={
        200: openapi.Response("Success", user),
        # 404: {'message': "User not found"},
        # 500: {'message': "Something went wrong!"}
    }
)
@api_view(['GET'])
def ContactById_View(request, *args, **kwargs):
    try:
        pk = kwargs.get('pk' or '')
        user = User.objects.get(pk=pk)
        serializer = getContact_Serializer(user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @swagger_auto_schema(
#     methods=['GET'],
#     responses={
#         200: {'user': getContact_Serializer()},
#         404: {'message': "User not found"},
#         500: {'message': "Something went wrong!"}
#     }
# )
@api_view(['GET'])
def ContactByUsername_View(request, *args, **kwargs):
    try:
        username = kwargs.get('username' or '')
        user = User.objects.get(username=username)
        serializer = getContact_Serializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'message': 'Something went wrong'})


@swagger_auto_schema(
    methods=['POST'],
    request_body=Login_Serializer()
)
@api_view(['POST'])
def Login_View(request, *args, **kwargs):
    serializer = Login_Serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['POST'],
    request_body=Logout_Serializer()
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def Logout_View(request, *args, **kwargs):
    serializer = Logout_Serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    methods=['POST'],
)
@api_view(['POST'])
# @permission_classes([IsAuthenticated, ResetPasswordPermission])
def ResetPassword_View(request, *args, **kwargs):
    try:
        username = kwargs.get('username' or '')
        user = User.objects.get(username=username)
        password = generate_Password()
        user.set_password(password)
        user.save()
        send_mail(
            "Password reset request",
            f"Your password reset.\nNew password: '{password}'",
            None,
            [user.email],
        )
        return Response({'message': "New password was sent to Email"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def ChangePassword_View(request, *args, **kwargs):
    user = request.user
    serializer = ChangePassword_Serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    if not user.check_password(data.get('old_password')):
        return Response({'message: Wrong old password'}, status=status.HTTP_400_BAD_REQUEST)
    if data.get('new_password') != data.get('new_password_dup'):
        return Response({'message: New passwords doesn\'t match'}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(data.get('new_password'))
    user.save()
    return Response({'message: New password was saved'})


@api_view(['POST'])
def Register_View(request, *args, **kwargs):
    serializer = Register_Serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    if User.objects.filter(email=data.get('email')).all().count() >= 1:
        return Response({"message": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    if data.get('password') != data.get('password_dup'):
        return Response({'message': "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
    # User.objects.create_user(**data)
    # TODO: After model is changed -> switch to commented one
    User.objects.create_user(
        username=data.get('username'), email=data.get('email'), password=data.get('password'),
        first_name=data.get('first_name'), last_name=data.get('last_name'), birthday=data.get('birthday'),
        phone=data.get('cell_phone'), address={
            'street':   data.get('street'),
            'city':     data.get('city'),
            'region':   data.get('region'),
            'country':  data.get('country'),
        }
    )
    login_serializer = Login_Serializer(data={'username': data.get('username'), 'password': data.get('password')})
    login_serializer.is_valid(raise_exception=True)
    return Response({"message": "Registered Successfully", **login_serializer.data}, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def ConfirmEmail(request, *args, **kwargs):


@api_view(['GET'])
def CheckEmailVal_View(request, *args, **kwargs):
    try:
        email = request.data.get('email')
        if not email:
            return Response({"message": "Email is not given"}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.get(email=email)
        return Response({'message': "Email is already taken.", 'valid': False}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'message': "Email is available.", 'valid': True}, status=status.HTTP_200_OK)


@api_view(['GET'])
def CheckUsernameVal_View(request, *args, **kwargs):
    try:
        username = request.data.get('username')
        if not username:
            return Response({"message": "Username is not given"}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.get(username=username)
        return Response({'message': 'Username is already taken.', 'valid': False}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'message': 'Username is available.', 'valid': True}, status=status.HTTP_200_OK)




