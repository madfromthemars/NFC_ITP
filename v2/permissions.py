# Rest
from rest_framework import permissions

# Local
from main.models import User
from .constants import USER_TYPE_ADMIN, USER_TYPE_COMPANY, USER_TYPE_REGULAR


class ResetPasswordPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.type in (USER_TYPE_ADMIN, USER_TYPE_COMPANY, USER_TYPE_REGULAR)

    def has_object_permission(self, request, view, obj):
        return (
            # Admin can reset password of any user
            request.user.type is USER_TYPE_ADMIN or
            # Company can change user
            (request.user.id == obj.created_by_id and request.user.type is USER_TYPE_COMPANY) or
            # User him/her + self can resset password
            request.user.id == obj.id
        )

