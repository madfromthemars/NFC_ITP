from rest_framework import permissions

from .models import User


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.type in ('ADMIN', 'COMPANY')
        elif view.action == 'create':
            return request.user.type in ('ADMIN', 'COMPANY')
        elif view.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return request.user.type != 'POLYGRAPHY'
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return obj == request.user or request.user.type == 'ADMIN' or obj.created_by_id == request.user.id


class OrderPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.type != "REGULAR"
        elif view.action == 'retrieve':
            return True
        elif view.action == 'create':
            return request.user.type != 'POLYGRAPHY'
        elif view.action in ('update', 'partial_update', 'destroy'):
            return request.user.type in ('ADMIN', 'POLYGRAPHY')
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ('list', 'retrieve'):
            try:
                user = User.objects.get(id=obj.user_id)
                return (
                        obj.user_id == request.user.id or
                        user.created_by_id == request.user.id or
                        request.user.type in ('ADMIN', 'POLYGRAPHY')
                )
            except User.DoesNotExist:
                return False
        elif view.action == 'create':
            try:
                user = User.objects.get(id=obj.user_id)
                return (
                        obj.user_id == request.user.id or
                        user.created_by_id == request.user.id or
                        request.user.type == 'ADMIN'
                )
            except User.DoesNotExist:
                return False
        return True


