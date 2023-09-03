from rest_framework import permissions


class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user making the request is a client user
        return request.user.is_authenticated and not request.user.is_superuser

