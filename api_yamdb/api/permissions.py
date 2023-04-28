from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class IsModerator(BasePermission):
    """Moderator role permission."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_moderator
                     or request.user.is_admin
                     or request.user.is_superuser))


class IsAdministrator(BasePermission):
    """Administrator role permission."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_superuser))


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    """Only owner, moderator & admins can edit or delete object permission."""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin)
