from rest_framework import permissions
from news.models import Event

class IsEventAuthorOrAdminOrReadOnly(permissions.BasePermission):

     def has_object_permission(self, request, view, event):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff is True or request.user == event.author:
            return True
        else:
            return False
