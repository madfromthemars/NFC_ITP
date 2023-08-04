from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    USER_TYPE_OPTIONS = [
        ("REGULAR", "Regular"),
        ("ADMIN", "Admin"),
        ("COMPANY", "Company | Manager"),
        ("POLYGRAPHY", "Polygraphy"),
    ]
    type = models.CharField(max_length=255, choices=USER_TYPE_OPTIONS, default="REGULAR")

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField(null=True)

    phone = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255)

    work_info = models.TextField(max_length=255, null=True)
    address = models.JSONField(max_length=255, null=True)

    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def get_clean_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'type': self.type,
            'phone': self.phone,
            'email': self.email,
            'birthday': self.birthday,
            'work_info': self.work_info,
            'address': self.address
        }

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Order(models.Model):
    STATUS_OPTIONS = [
        ("NEW", "New"),
        ("IN PROCESS", "In process"),
        ("READY", "Ready"),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=255, default="NEW", choices=STATUS_OPTIONS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' - ' + self.status
