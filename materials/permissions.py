from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """Класс проверящий является ли пользователья модератором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Модераторы").exists()


class IsOwner(BasePermission):
    """Класс проверящий является ли пользователья владельцем"""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False
