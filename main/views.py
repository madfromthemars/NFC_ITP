from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http.response import FileResponse
from .permission import UserPermissions, OrderPermissions
from django.db.utils import IntegrityError

# Local 
from .models import User, Order
from .serializers import (RegisterSerializer, LoginSerializer, LogoutSerializer,
                          UserSerializer, OrderSerializer)
from .utils import VCardFile


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            user = User.objects.get(username=request.data.get('username'))
            VCardFile(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = User.objects.get(username=data.get('username'))
        res = {
            'tokens': data.get('tokens'),
            'user': user.get_clean_dict()
        }
        if user.type == "REGULAR":
            orders = Order.objects.filter(user_id=user.id).all()
            try:
                company = User.objects.get(id=user.created_by_id).get_clean_dict()
            except User.DoesNotExist:
                company = None
            res['user']['orders'] = OrderSerializer(orders, many=True).data
            res['user']['company'] = company
        elif user.type == "COMPANY":
            # Number of users
            NoU = User.objects.filter(created_by=user.id).count()
            NoU_orders_new = Order.objects.filter(user_id__created_by=user.id,
                                                  status="NEW").count()
            NoU_orders_process = Order.objects.filter(user_id__created_by=user.id,
                                                      status="IN PROCESS").count()
            NoU_orders_ready = Order.objects.filter(user_id__created_by=user.id,
                                                    status="READY").count()
            res['data'] = {
                'Num_Users': NoU,
                'NumUser_Orders': {
                    'new': NoU_orders_new,
                    'process': NoU_orders_process,
                    'ready': NoU_orders_ready},
            }
        elif user.type == "POLYGRAPHY":
            Num_Orders_tot = Order.objects.count()
            Num_Orders_new = Order.objects.filter(status="NEW").count()
            Num_Orders_proc = Order.objects.filter(status="IN PROCESS").count()
            Num_Orders_read = Order.objects.filter(status="READY").count()
            res['data'] = {
                'orders': {
                    'tot': Num_Orders_tot,
                    'new': Num_Orders_new,
                    'process': Num_Orders_proc,
                    'ready': Num_Orders_read
                }
            }

        return Response(data=res, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        try:
            user = User.objects.get(username=username).get_clean_dict()
            return Response(data=user, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class VCardAPIView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        try:
            user = User.objects.get(username=username)
            return FileResponse(open(f'./files/user_{user.id}.vcf', 'rb'))
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, UserPermissions)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        if request.user.type == "COMPANY":
            queryset = User.objects.filter(created_by=request.user.id).all()
            serializer = self.serializer_class(queryset, many=True)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            if request.user.type == 'COMPANY':
                request.data['created_by_id'] = request.user.id
            serialized = self.serializer_class(data=request.data)
            serialized.is_valid(raise_exception=True)
            serialized.save()
            user = User.objects.get(username=request.data.get('username'))
            VCardFile(user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message": "Problem with creating VCF file"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'message': "User with such username already exists"}, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        try:
            pk = kwargs.get("pk", None)
            user = User.objects.get(id=pk)
            serializer = self.serializer_class(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            VCardFile(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message": "Problem with creating VCF file"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'message': "User with such username already exists"}, status=status.HTTP_409_CONFLICT)


class OrderViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, OrderPermissions)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        if request.user.type == "COMPANY":
            queryset = Order.objects.filter(user__created_by_id=request.user.id).all()
            serializer = self.serializer_class(queryset, many=True)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get('user_id'))
            _n = Order.objects.filter(user_id=user.id).exclude(status="READY").count()
            if _n >= 1 and request.user.type != "ADMIN":
                return Response({'message': "User already has order in queue"}, status=status.HTTP_400_BAD_REQUEST)
            elif user.id != request.user.id and request.user.type != "ADMIN" and user.created_by_id != request.user.id:
                return Response({"message": "You do not have permission to perform this action."},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': "User doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
