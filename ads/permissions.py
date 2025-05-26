from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение: только владелец объекта может редактировать или удалять его.
    Для чтения доступно всем.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Только владелец (user) может изменять/удалять
        return obj.user == request.user


class IsReceiverOrReadOnly(permissions.BasePermission):
    """
    Разрешение: только получатель предложения может изменять его (например, менять статус).
    Для чтения доступно всем.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Только получатель предложения может менять статус или удалять
        return obj.ad_receiver.user == request.user
