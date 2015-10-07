from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from chat.filters import PostFilter
from chat.serializers import ChannelSerializer, ChannelMemberSerializer, ChannelGroupSerializer, PostSerializer
from chat.models import Channel, ChannelMember, ChannelGroup, Post

@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
class ChannelView(ListModelMixin,
                  CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
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
        filter_backends = (DjangoFilterBackend, SearchFilter,)
        search_fields = ('name',)
        # TODO: filter_class = ChannelFilter

@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
class ChannelMemberView(ListModelMixin,
                        CreateModelMixin,
                        RetrieveModelMixin,
                        DestroyModelMixin,
                        viewsets.GenericViewSet):
        """
        === Many to many relationship for user based channels ===

        Only admins or channel owners are allowed to POST or DELETE entries.
        """

        queryset = ChannelMember.objects.all()
        serializer_class = ChannelMemberSerializer

@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
class ChannelGroupView(ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       DestroyModelMixin,
                       viewsets.GenericViewSet):
        """
        === Many to many relationship for group based channels ===

        Only admins or channel owners are allowed to POST or DELETE entries.
        """

        queryset = ChannelGroup.objects.all()
        serializer_class = ChannelGroupSerializer

@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
class PostViewSet(ListModelMixin,
                  CreateModelMixin,
                  RetrieveModelMixin,
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
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('content',)
    filter_class = PostFilter

    def perform_create(self, serializer):
        """
        Connected users should be able to send `m` posts from the user
        interface. Any other kind of post that could be displayed to users
        should be created by backend applications triggered by requests sent to
        the API.
        """

        serializer.save(author=self.request.user, type='m')
