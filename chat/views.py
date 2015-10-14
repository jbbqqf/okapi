from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from guardian.shortcuts import get_users_with_perms, get_groups_with_perms

from chat.filters import PostFilter, ReadablePostFilter
from chat.serializers import ChannelSerializer, PostSerializer
from chat.models import Channel, Post

@authentication_classes((TokenAuthentication, SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))#IsChannelMember,))
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

# @authentication_classes((SessionAuthentication, BasicAuthentication,))
# @permission_classes((IsAuthenticated,))
# class ChannelMemberView(APIView):
#         """
#         === Many to many relationship for user based channels ===
# 
#         Only admins or channel owners are allowed to POST or DELETE entries.
#         """
# 
#         # queryset = None
#         # serializer_class = ChannelMemberSerializer
# 
#         def retrieve(self, request, pk=None):    
#             channel = self.get_object()
#             perms = get_users_with_perm(channel, attach_perms=True)
#             return Response(perms)

# @authentication_classes((SessionAuthentication, BasicAuthentication,))
# @permission_classes((IsAuthenticated,))
# class ChannelGroupView(ListModelMixin,
#                        CreateModelMixin,
#                        RetrieveModelMixin,
#                        DestroyModelMixin,
#                        viewsets.GenericViewSet):
#         """
#         === Many to many relationship for group based channels ===
# 
#         Only admins or channel owners are allowed to POST or DELETE entries.
#         """
# 
#         queryset = None
#         serializer_class = ChannelGroupSerializer
# 
#         def retrieve(self, request, pk=None):
#             channel = self.get_object()
#             perms = get_groups_with_perm(channel, attach_perms=True)
#             return Response(perms)

@authentication_classes((TokenAuthentication, SessionAuthentication, BasicAuthentication,))
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
    filter_backends = (ReadablePostFilter, DjangoFilterBackend, SearchFilter,)
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
