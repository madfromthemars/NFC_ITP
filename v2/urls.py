# Django
from django.urls import path

# Local
from .views import (
    Register_View, Login_View, ResetPassword_View, ChangePassword_View, ContactById_View, ContactByUsername_View,
    CheckEmailVal_View, CheckUsernameVal_View,
)

urlpatterns = [
    path('auth/register/', Register_View, name='register-v2' ),
    path('auth/login/', Login_View, name='login-v2'),
    path('auth/reset-password/<str:username>/', ResetPassword_View, name='resset-password-v2'),
    path('auth/change-password/', ChangePassword_View, name='change-password-v2'),
    path('auth/check-available/email/', CheckEmailVal_View, name='check-available-email-v2'),
    path('auth/check-available/username/', CheckUsernameVal_View, name='check-available-username-v2'),

    path('contact/pk/<int:pk>', ContactById_View, name='contact-id-v2'),
    path('contact/username/<str:username>', ContactByUsername_View, name='contact-username-v2')
]

