# -*- coding: utf-8 -*-

from rest_framework.permissions import (
    BasePermission, SAFE_METHODS, IsAdminUser)


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, profile):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        return IsAdminUser()
