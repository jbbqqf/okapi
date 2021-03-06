# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.decorators import (
    authentication_classes, permission_classes)
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from common.permissions import IsAdminOrReadOnly
from groups.serializers import GroupSerializer
from groups.models import Group
from groups.filters import GroupFilter


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,))
class GroupViewSet(viewsets.ModelViewSet):
    """
    === This set of groups includes both promotions and clubs ===

    You can imagine many things to be regrouped in groups. Groups are
    especially designed to handle promotions (hence the parent attribute) and
    clubs, which are natural groups related to Telecom. But it is also possible
    to tag people for some random reasons.

    Parent field must be provided, and should refer a virtual root group if the
    group you want to create is supposed to be a top-level group.

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
    search_fields = ('name', 'url', 'mailing', 'description',)
    filter_class = GroupFilter
