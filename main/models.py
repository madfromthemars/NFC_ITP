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
    birthday = models.DateField(null=True, blank=True)

    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True)

    work_info = models.JSONField(max_length=255, null=True, blank=True)
    address = models.JSONField(max_length=255, null=True, blank=True)

    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    theme = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        return self.username

    def get_clean_dict(self):
        company = None
        if self.created_by:
            company = self.created_by.id

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
            'address': self.address,
            'created_by_id': company,
            'theme': self.theme
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
