from rest_framework import permissions

from fileshare.models import File, Directory

class IsFileOwnerOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, file):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff is True or request.user == file.owner:
            return True
        else:
            return False

class CanEditDirectory(permissions.BasePermission):
    """
    When a user tries to edit a directory, it is first checked that requested
    operation does not concern root directory, which is forbidden for anyone.

    If a user wants to destroy a directory, some tests make sure it does not
    have any childs, in which case operation is not allowed.
    """

    def has_object_permission(self, request, view, directory):
        if request.method not in permissions.SAFE_METHODS:
            if directory.parent is None:
                return False

            if request.method == 'DELETE':
                dir_childs = Directory.objects.filter(parent=directory).exists()
                file_childs = File.objects.filter(parent=directory).exists()

                if (dir_childs or file_childs) is True:
                    return False

        return True
