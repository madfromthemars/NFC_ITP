from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

# Local
from .views import (RegisterView, LoginAPIView, LogoutAPIView,
                    UserViewSet, OrderViewSet, ContactAPIView, VCardAPIView)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('contact/<int:username>', ContactAPIView.as_view(), name='contact'),
    path('vcard/<str:username>', VCardAPIView.as_view(), name='vcard'),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
]
