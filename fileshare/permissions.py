# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission, SAFE_METHODS
from fileshare.models import File, Directory


class IsFileOwnerOrAdminOrReadOnly(BasePermission):
    """
    Everyone can read files but only staff or owners can edit / delete it.
    """

    def has_object_permission(self, request, view, file):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff is True or request.user == file.creator:
            return True

        return False


class CanEditDirectory(BasePermission):
    """
    When a user tries to edit a directory, it is first checked that requested
    operation does not concern root directory, which is forbidden for anyone.

    If a user wants to destroy a directory, some tests make sure it does not
    have any childs, in which case operation is not allowed.
    """

    def has_object_permission(self, request, view, directory):
        if request.method not in SAFE_METHODS:
            if directory.parent is None:
                return False

            if request.method == 'DELETE':
                dir_childs_query = Directory.objects.filter(parent=directory)
                dir_childs_exist = dir_childs_query.exists()

                file_childs_query = File.objects.filter(parent=directory)
                file_childs_exist = file_childs_query.exists()

                if (dir_childs_exist or file_childs_exist) is True:
                    return False

        return True
