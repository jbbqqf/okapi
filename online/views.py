# -*- coding: utf-8 -*-

from datetime import datetime

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import (
    authentication_classes, permission_classes, list_route)
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.permissions import AllowAny
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from online.filters import PresenceFilter
from online.models import Presence
from online.serializers import PresenceSerializer


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((AllowAny,))
class PresenceView(ReadOnlyModelViewSet):
    """
    User interfaces decide when to push informations and whether they want
    to use stuff here. Since okapi is a stateless web service and can handle
    multiple clients, there is no way to force users to show their presence.

    However, if the client implementation wants to offer this feature to make
    chat discussions more convenient, Presence objects offer this possibility.

    The last_active field should be updated frequently to inform that
    connected user has used his mouse, clicked or triggered something on the
    interface. If the interface environment allows it, a running client can
    also update it to inform that his user is still connected but hasn't been
    active.
    """

    queryset = Presence.objects.all()
    serializer_class = PresenceSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PresenceFilter

    @list_route(methods=['POST'])
    def active(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            message = {
                'message': 'You must authenticate to perform this action'}
            return Response(message, status=HTTP_401_UNAUTHORIZED)

        presence, created = Presence.objects.get_or_create(
            user=request.user)

        now = datetime.now()
        presence.last_passive = now
        presence.last_active = now

        presence.save()

        serializer = self.get_serializer(presence)
        return Response(serializer.data)

    @list_route(methods=['POST'])
    def passive(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            message = {
                'message': 'You must authenticate to perform this action'}
            return Response(message, status=HTTP_401_UNAUTHORIZED)

        presence, created = Presence.objects.get_or_create(
            user=request.user)

        now = datetime.now()
        presence.last_passive = now

        presence.save()

        serializer = self.get_serializer(presence)
        return Response(serializer.data)
