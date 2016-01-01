# -*- coding: utf-8 -*-

from rest_framework.viewsets import GenericViewSet
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN)
from rest_framework.response import Response
from rest_framework.decorators import (
    authentication_classes, permission_classes, detail_route)
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from guardian.shortcuts import (
    get_users_with_perms, get_groups_with_perms, assign_perm, remove_perm)
from guardian.utils import clean_orphan_obj_perms

from chat.filters import (
    PostFilter, ReadablePostFilter, ChannelFilter, ReadableChannelFilter)
from chat.serializers import (ChannelSerializer, ChannelMemberSerializer,
                              ChannelGroupSerializer, PostSerializer)
from chat.models import Channel, Post
from chat.permissions import (IsChannelAdminOrReadOnly,
                              IsChannelWriterOrReadOnly)
from chat.pagination import PostsPagination
from profiles.models import User
from groups.models import Group


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated, IsChannelAdminOrReadOnly,))
class ChannelView(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    """
    === Allows users to chat on different public or private channels ===

    Channels are Post containers filtering who can read/write where. They are
    mainly supposed to provide a channel for each promo and for each club group
    as well as a default public channel. It is also possible to create a
    channel where only two users can read/write for private messaging.

    Default general channel which id is 1 is a channel where anyone can
    read/write. It's permissions cannot be edited by anyone.

    When a user peform a GET query on /chat/channels/, only channels where the
    user or one of his group have at least read rights are returned.

    ---

    list:
        parameters:
            - name: search
              description: contain filter for name
              paramType: query
              type: string

    retrieve:
        parameters:
            - name: search
              description: contain filter for name
              paramType: query
              type: string
    """

    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = (ReadableChannelFilter,
                       DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    filter_class = ChannelFilter

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        channel = serializer.save()

        # Request initiator is graunted admin rights on creation
        assign_perm('read_channel', request.user, channel)
        assign_perm('write_channel', request.user, channel)
        assign_perm('admin_channel', request.user, channel)

        return Response(serializer.data, status=HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        clean_orphan_obj_perms()
        return Response(status=HTTP_204_NO_CONTENT)

    @detail_route()
    def userperms(self, request, pk=None):
        """
        === Return a list of users with their permissions ===

        Keep in mind that not only user permissions are checked, but also
        group dependant permissions.

        For exemple : userA has no permission on chanA. But userA is in groupA.
        groupA has write_perm on chanA. So userA will be mentionned by
        /userperms/.
        """

        channel = self.get_object()
        perms = get_users_with_perms(channel, attach_perms=True)

        serialized_perms = []
        for user, perm in perms.items():
            temp_perm = {}
            temp_perm['user'] = user.id
            temp_perm['permissions'] = perm
            serialized_perms.append(temp_perm)

        return Response(serialized_perms)

    @detail_route()
    def myperms(self, request, pk=None):
        """
        === Return permissions requesting user has ===
        """

        channel = self.get_object()
        me = request.user

        permissions = {}
        for perm in ['read_channel', 'write_channel', 'admin_channel']:
            permissions[perm] = me.has_perm(perm, channel)

        return Response(permissions)

    @detail_route(methods=['POST'])
    def adduser(self, request, pk=None):
        """
        === Add a user permission ===

        FORMS PROVIDED BY AUTO-GENERATED DOCUMENTATION ARE NOT CORRECT. REFER
        TO FOLLOWING INSTRUCTIONS TO REQUEST ON THIS ROUTE :

        You need to provide those fields in POST parameters :
          * user : user id
          * permissions : `read_channel`, `write_channel` or `admin_channel`

        Keep in mind that permissions are inclusive. admin_channel includes
        write_channel which includes read_channel.

        If you give admin_channel permissions, you will also give both
        read_channel and write_channel.
        """

        channel = self.get_object()

        serializer = ChannelMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.data['user']
        user = User.objects.get(pk=user_id)
        permission = serializer.data['permissions']

        # To avoid mistakes if a user is granted write rights, it's also
        # true for read ones. Well this is discutable...
        if permission == 'write_channel':
            assign_perm('read_channel', user, channel)

        # Same thing for admin rights toward write and read ones
        if permission == 'admin_channel':
            assign_perm('read_channel', user, channel)
            assign_perm('write_channel', user, channel)

        # In the end of the process we give the user his supplied rights
        assign_perm(permission, user, channel)

        message = {
            'message':
            'User {} can {} {}'.format(user, permission, channel)
        }
        return Response(message)

    @detail_route(methods=['POST'])
    def rmuser(self, request, pk=None):
        """
        === Remove a user permission ===

        FORMS PROVIDED BY DOCUMENTATION ARE NOT CORRECT. REFER TO FOLLOWING
        INSTRUCTIONS TO REQUEST ON THIS ROUTE :

        You need to provide those fields in POST parameters :
          * user : user id
          * permissions : `read_channel`, `write_channel` or `admin_channel`

        Keep in mind that permissions are inclusive. admin_channel includes
        write_channel which includes read_channel.

        If you remove read_channel permissions, you will also remove both
        write_channel and admin_channel.
        """

        channel = self.get_object()

        serializer = ChannelMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.data['user']
        user = User.objects.get(pk=user_id)
        permission = serializer.data['permissions']

        # As for adduser route we remove included permissions if necessary
        if permission == 'write_channel':
            remove_perm('admin_channel', user, channel)

        if permission == 'read_channel':
            remove_perm('write_channel', user, channel)
            remove_perm('admin_channel', user, channel)

        remove_perm(permission, user, channel)

        message = {
            'message':
            'User {} can not {} {} anymore'.format(
                user, permission, channel)
        }
        return Response(message)

    @detail_route()
    def groupperms(self, request, pk=None):
        """
        === Return a list of group with their permissions ===
        """

        channel = self.get_object()
        perms = get_groups_with_perms(channel, attach_perms=True)

        serialized_perms = []
        for group, perm in perms.items():
            temp_perm = {}
            temp_perm['group'] = group.id
            temp_perm['permissions'] = perm
            serialized_perms.append(temp_perm)

        return Response(serialized_perms)

    @detail_route(methods=['POST'])
    def addgroup(self, request, pk=None):
        """
        === Add a group permission ===

        FORMS PROVIDED BY DOCUMENTATION ARE NOT CORRECT. REFER TO FOLLOWING
        INSTRUCTIONS TO REQUEST ON THIS ROUTE :

        You need to provide those fields in POST parameters :
          * group : group id
          * permissions : `read_channel`, `write_channel` or `admin_channel`

        Keep in mind that permissions are inclusive. admin_channel includes
        write_channel which includes read_channel.

        If you give admin_channel permissions, you will also give both
        read_channel and write_channel.
        """

        channel = self.get_object()

        serializer = ChannelGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_id = serializer.data['group']
        group = Group.objects.get(pk=group_id)
        permission = serializer.data['permissions']

        # To avoid mistakes if a group is granted write rights, it's also
        # true for read ones. Well this is discutable...
        if permission == 'write_channel':
            assign_perm('read_channel', group, channel)

        # Same thing for admin rights toward write and read ones
        if permission == 'admin_channel':
            assign_perm('read_channel', group, channel)
            assign_perm('write_channel', group, channel)

        # In the end of the process we give the user his supplied rights
        assign_perm(permission, group, channel)

        message = {
            'message':
            'Group {} can {} {}'.format(group, permission, channel)
        }
        return Response(message)

    @detail_route(methods=['POST'])
    def rmgroup(self, request, pk=None):
        """
        === Remove a group permission ===

        FORMS PROVIDED BY DOCUMENTATION ARE NOT CORRECT. REFER TO FOLLOWING
        INSTRUCTIONS TO REQUEST ON THIS ROUTE :

        You need to provide those fields in POST parameters :
          * group : group id
          * permissions : `read_channel`, `write_channel` or `admin_channel`

        Keep in mind that permissions are inclusive. admin_channel includes
        write_channel which includes read_channel.

        If you remove read_channel permissions, you will also remove both
        write_channel and admin_channel.
        """

        channel = self.get_object()

        serializer = ChannelGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_id = serializer.data['group']
        group = Group.objects.get(pk=group_id)
        permission = serializer.data['permissions']

        # As for addgroup route we remove included permissions if necessary
        if permission == 'write_channel':
            remove_perm('admin_channel', group, channel)

        if permission == 'read_channel':
            remove_perm('write_channel', group, channel)
            remove_perm('admin_channel', group, channel)

        remove_perm(permission, group, channel)

        message = {
            'message':
            'Group {} can not {} {} anymore'.format(
                group, permission, channel)
        }
        return Response(message)


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated, IsChannelWriterOrReadOnly,))
class PostViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    """
    === Post objects are messages broadcasted in channels  ===

    You can perform GET or POST requests on post objects only if you are
    authenticated. The reason for this is we don't want people from the outside
    to be able to read random cynical, sexist and hyper-sexualized
    conversations.

    For the moment, the only type of post a connected user can POST are
    messages (`m`) : it is automaticaly set. In the future we can imagine other
    applications being able to broadcast messages in channels such as games
    sending score notifications.

    Current user as author and current datetime are be recorded in the
    database without having to provide it. It is possible to access those
    fields when performing GET requests.

    Since posts depend on channels they are broadcasted to, a user requesting
    /chat/posts/ route will be only able to see posts refering to channels
    where he has read_channel rights.

    Posts can not be edited... excepted by admins in the admin interface if
    necessary.

    ---

    list:
        parameters:
            - name: search
              description: contain filter for content
              paramType: query
              type: string

    retrieve:
        parameters:
            - name: search
              description: contain filter for content
              paramType: query
              type: string
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (ReadablePostFilter, DjangoFilterBackend, SearchFilter,)
    search_fields = ('content',)
    filter_class = PostFilter
    pagination_class = PostsPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        channel = serializer.validated_data['channel']

        if channel.public is True:
            self.perform_create(serializer)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if request.user.has_perm('chat.write_channel', channel):
            self.perform_create(serializer)
            return Response(serializer.data, status=HTTP_201_CREATED)

        message = {'detail':
                   'You do not have permission to perform this action.'}
        return Response(message, status=HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        """
        Connected users should be able to send `m` posts from the user
        interface. Any other kind of post that could be displayed to users
        should be created by backend applications triggered by requests sent to
        the API.
        """

        serializer.save(author=self.request.user, type='m')
