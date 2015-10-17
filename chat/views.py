from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, detail_route
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.status import HTTP_400_BAD_REQUEST

from guardian.shortcuts import get_users_with_perms, get_groups_with_perms, assign_perm, remove_perm
from guardian.utils import clean_orphan_obj_perms

from chat.filters import PostFilter, ReadablePostFilter, ReadableChannelFilter
from chat.serializers import ChannelSerializer, ChannelMemberSerializer, ChannelGroupSerializer, PostSerializer
from chat.models import Channel, Post
from chat.permissions import IsChannelAdminOrReadOnly, IsChannelWriterOrReadOnly
from profiles.models import User
from groups.models import Group

@authentication_classes((TokenAuthentication, SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated, IsChannelAdminOrReadOnly,))
class ChannelView(ListModelMixin,
                  RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    === Allows users to chat on different public or private channel ===

    Channels are supposed to provide mainly a channel by promo and by
    club group as well as a default public channel.

    Default channel which id is 1 cannot be edited by anyone. Other channel
    are only visible for members of the channel or members of one group
    associed to the channel.

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
    filter_backends = (ReadableChannelFilter, DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    # TODO: filter_class = ChannelFilter

    # TODO: give correct permissions on create / delete and check on update
    # TODO: remove mixins

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        channel = serializer.save()

        # Request initiator is graunted admin rights on creation
        assign_perm('read_channel', request.user, channel)
        assign_perm('write_channel', request.user, channel)
        assign_perm('admin_channel', request.user, channel)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        clean_orphan_obj_perms()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route()
    def userperms(self, request, pk=None):
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
        channel = self.get_object()
        me = request.user

        permissions = {}
        for perm in ['read_channel', 'write_channel', 'admin_channel']:
            permissions[perm] = me.has_perm(perm, channel)

        return Response(permissions)

    @detail_route(methods=['post'])
    def adduser(self, request, pk=None):
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

    @detail_route(methods=['post'])
    def rmuser(self, request, pk=None):
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
        channel = self.get_object()
        perms = get_groups_with_perms(channel, attach_perms=True)

        serialized_perms = []
        for group, perm in perms.items():
            temp_perm = {}
            temp_perm['group'] = group.id
            temp_perm['permissions'] = perm
            serialized_perms.append(temp_perm)
        
        return Response(serialized_perms)

    @detail_route(methods=['post'])
    def addgroup(self, request, pk=None):
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

    @detail_route(methods=['post'])
    def rmgroup(self, request, pk=None):
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

@authentication_classes((TokenAuthentication, SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated, IsChannelWriterOrReadOnly,))
class PostViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    === Post objects provides data for a chat application  ===

    You can only perform GET or POST requests on post objects if you are
    authenticated. The reason for this is we don't want people from the outside
    to be able to read random cynical, sexist and hyper-sexualized
    conversations.

    For the moment, the only type of post a connected user can POST are messages
    (`m`). In the future we can imagine games to be accessible from the API and
    score notifications will be displayed as messages.

    The only field you need to provide when a user writes a message is its
    content. Current user and current datetime will be recorded in the base but
    you will be able to access those fields only when performing GET requests.

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        channel = serializer.validated_data['channel']

        if channel.public is True:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.user.has_perm('chat.write_channel', channel):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        message = {'detail':
                   'You do not have permission to perform this action.'}
        return Response(message, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        """
        Connected users should be able to send `m` posts from the user
        interface. Any other kind of post that could be displayed to users
        should be created by backend applications triggered by requests sent to
        the API.
        """

        serializer.save(author=self.request.user, type='m')
