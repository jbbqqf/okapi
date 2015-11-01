# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEventAuthorOrAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, event):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff is True or request.user == event.author:
            return True

        else:
            return False
