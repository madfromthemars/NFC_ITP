from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'type', 'first_name', 'last_name', 'birthday', 'phone', 'email',
            'work_info', 'address', 'created_by'
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'type', 'first_name', 'last_name', 'birthday', 'phone', 'email',
            'work_info', 'address', 'created_by'
        )
