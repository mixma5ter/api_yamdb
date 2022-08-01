from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """Доступ только для чтения. У админа полный доступ."""

    def has_permission(self, request, view):
        user = request.user
        return (request.method in permissions.SAFE_METHODS
                or user.is_authenticated and user.is_admin)

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (request.method in permissions.SAFE_METHODS
                or user.is_authenticated and user.is_admin)


class IsAdmin(permissions.BasePermission):
    """Доступ только у админа."""

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_admin

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.is_admin


class IsAuthorOrStaff(permissions.BasePermission):
    """Доступ только для чтения. У админа и автора полный доступ."""

    def has_permission(self, request, view):
        user = request.user
        return (request.method in permissions.SAFE_METHODS
                or user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (request.method in permissions.SAFE_METHODS
                or user.is_moderator
                or user.is_admin
                or obj.author == request.user)
