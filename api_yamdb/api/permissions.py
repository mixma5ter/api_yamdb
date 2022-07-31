from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """ Доступ только для чтения. У админа полный доступ. """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin() or request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin() or request.user.is_superuser
        return False


class IsAdmin(permissions.BasePermission):
    """ Permission for admin. """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin() or request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_admin() or request.user.is_superuser
        return False


class IsAuthorOrStaff(permissions.BasePermission):
    """ Permission for comments. """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator()
            or request.user.is_admin()
            or request.user.is_superuser
        )