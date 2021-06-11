from rest_framework import permissions


class IsOwnerOrAdmin(permissions.IsAuthenticated):
    """
    Object-level permission to only allow owners of an object or admins to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user or request.user.is_staff is True
