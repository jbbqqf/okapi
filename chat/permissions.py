from rest_framework import permissions

class IsChannelAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only users having admin_channel rights on a
    given channel to perform write actions.

    It also prevents anyone to edit default general channel.

    This permission does not filter which channel can be seen (refering to
    read_channel rights) : this is ReadableChannelFilter's job.
    """

    def has_object_permission(self, request, view, channel):
        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            # id 1 is supposed to be default general channel
            if channel.id == 1:
                return False
            
            if request.user.has_perm('chat.admin_channel', channel):
                return True

            else:
                return False
