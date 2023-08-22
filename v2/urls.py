# Django
from django.urls import path

# Local
from .views import (Login_View, ResetPassword_View,
                    ContactById_View, ContactByUsername_View)

urlpatterns = [
    path('auth/login', Login_View, name='login-v2'),
    path('auth/resset-password/<str:username>/', ResetPassword_View, name='resset-password-v2'),

    path('contact/pk/<int:pk>', ContactById_View, name='contact-id-v2'),
    path('contact/username/<str:username>', ContactByUsername_View, name='contact-username-v2')
]

