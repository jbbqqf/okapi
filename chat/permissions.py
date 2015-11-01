# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsChannelAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only users having admin_channel rights on a
    given channel to perform write actions.

    It also prevents anyone to edit default general channel.

    This permission does not filter which channel can be seen (refering to
    read_channel rights) : this is ReadableChannelFilter's job.
    """

    def has_object_permission(self, request, view, channel):
        if request.method in SAFE_METHODS:
            return True

        else:
            # id 1 is supposed to be default general channel
            if channel.id == 1:
                return False

            if channel.public is True:
                return True

            if request.user.has_perm('chat.admin_channel', channel):
                return True

            else:
                return False


class IsChannelWriterOrReadOnly(BasePermission):
    """
    Custom permission to allow only users having write_channel rights on a
    given channel to post messages on that channel.

    If channel is public, any message from any source will be accepted.
    """

    def has_object_permission(self, request, view, post):
        if request.method in SAFE_METHODS:
            return True

        else:
            if post.channel.public is True:
                return True

            if request.user.has_perm('chat.write_channel', post.channel):
                return True

            else:
                return False
