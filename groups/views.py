from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import detail_route, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin

from common.permissions import IsAdminOrReadOnly
from groups.serializers import GroupSerializer, GroupUserSerializer, okaGroupSerializer
from profiles.serializers import UserSerializer
from groups.models import Group, GroupUser, okaGroup, get_group_members
from groups.filters import GroupFilter

@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,))
class okaGroupViewSet(viewsets.ModelViewSet):
    queryset = okaGroup.objects.all()
    serializer_class = okaGroupSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ['name', 'url', 'mailing', 'description',]
    # TODO: filter_class = okaGroupFilter

@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,))
class GroupViewSet(viewsets.ModelViewSet):
    """
    === This set of groups includes both promotions and clubs ===

    You can imagine many things to be regrouped in groups. Groups are especially
    designed to handle promotions (hence the parent attribute) and clubs, which
    are natural groups related to Telecom. But it is also possible to tag people
    for some random reasons.

    Parent field must be provided, and should refer a virtual root group if the
    group you want to create is supposed to be a top-level group.

    Only admins are allowed to update groups but anyone is able to read groups.

    ---
    
    list:
        parameters:
            - name: search
              description: contain filter for name, url, mailing or description
              paramType: query
              type: string

    retrieve:
        parameters:
            - name: search
              description: contain filter for name, url, mailing or description
              paramType: query
              type: string
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ['name', 'url', 'mailing', 'description']
    filter_class = GroupFilter

    @detail_route()
    def users(self, request, pk=None):
        """
        Allows to request all users a group regroups.
        """

        group = self.get_object()

        users = get_group_members(group)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,))
class GroupUserViewSet(ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       DestroyModelMixin,
                       viewsets.GenericViewSet):
    """
    === Many to many relationship to describe membership ===

    Appart from user and group id, role is the last argument available here,
    which is described by a single letter.

    Only admins are allowed to POST or DELETE entries here.
    """

    queryset = GroupUser.objects.all()
    serializer_class = GroupUserSerializer
