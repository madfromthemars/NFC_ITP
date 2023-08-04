from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, Order


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'type')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('type', 'birthday', 'phone',
                           'work_info', 'address', 'created_by'
                           )}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('type', 'first_name', 'last_name', 'birthday', 'phone', 'email',
                           'work_info', 'address', 'created_by'
                           )}),)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Order)
