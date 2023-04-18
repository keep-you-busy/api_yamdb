from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminModeratorAuthorPermission(BasePermission):
    """Редактировать и удалять пост может только владелец."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
