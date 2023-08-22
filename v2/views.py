# Rest
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

# Local
from .serializers import  getContact_Serializer, Login_Serializer
from main.models import User
from .utils import generate_Password
from .permissions import ResetPasswordPermission

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


@api_view(['POST'])
def Login_View(request, *args, **kwargs):
    serializer = Login_Serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([ResetPasswordPermission])
def ResetPassword_View(request, *args, **kwargs):
    try:
        username = kwargs.get('username' or '')
        user = User.objects.get(username=username)
        password = generate_Password()
        user.set_password(password)
        user.save()
        return Response({'message': 'New password sent to your e-mail address.', 'password': password}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


