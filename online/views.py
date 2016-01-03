# -*- coding: utf-8 -*-

from datetime import datetime

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import (
    authentication_classes, permission_classes, api_view)
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from common.common import get_ip, get_first_proxy_ip
from online.filters import PresenceFilter
from online.models import Presence
from online.serializers import (
    PresenceSerializer, IPPrivacySerializer, AwaySerializer)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def active(request, *args, **kwargs):
    """
    === Notify an active presence ===

    You can provide one, two or none of those fields in POST parameters :
      * show_ip : true or false (default is true)
      * show_proxy_ip : true or false (default is true)

    Notifying an active presence will also update user's passive presence.
    """

    ip_privacy_serializer = IPPrivacySerializer(data=request.data)
    ip_privacy_serializer.is_valid(raise_exception=True)

    presence, created = Presence.objects.get_or_create(
        user=request.user)

    now = datetime.now()
    # an active presence includes the fact that user is passively present
    presence.last_passive = now
    presence.last_active = now

    if ip_privacy_serializer.data['show_ip'] is True:
        # well, we try and if the output data of get_ip doesn't work we
        # just make sure to ecrase previous value
        try:
            presence.ip = get_ip(request)
        except:
            presence.ip = None
    else:
        # this is important to set it to None to ecrase any previous
        # potential value
        presence.ip = None

    if ip_privacy_serializer.data['show_proxy_ip'] is True:
        # well, we try and if the output data of get_first_proxy_ip
        # doesn't work we just make sure to ecrase previous value
        try:
            presence.proxy_ip = get_first_proxy_ip(request)
        except:
            presence.proxy_ip = None
    else:
        # this is important to set it to None to ecrase any previous
        # potential value
        presence.proxy_ip = None

    presence.save()

    response_serializer = PresenceSerializer(presence)
    if created:
        status = HTTP_201_CREATED
    else:
        status = HTTP_200_OK

    return Response(response_serializer.data, status=status)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def passive(request, *args, **kwargs):
    """
    === Notify a passive presence ===

    You can provide one, two or none of those fields in POST parameters :
      * show_ip : true or false (default is true)
      * show_proxy_ip : true or false (default is true)
    """

    ip_privacy_serializer = IPPrivacySerializer(data=request.data)
    ip_privacy_serializer.is_valid(raise_exception=True)

    presence, created = Presence.objects.get_or_create(
        user=request.user)

    now = datetime.now()
    presence.last_passive = now

    if ip_privacy_serializer.data['show_ip'] is True:
        # well, we try and if the output data of get_ip doesn't work we
        # just make sure to ecrase previous value
        try:
            presence.ip = get_ip(request)
        except:
            presence.ip = None
    else:
        # this is important to set it to None to ecrase any previous
        # potential value
        presence.ip = None

    if ip_privacy_serializer.data['show_proxy_ip'] is True:
        # well, we try and if the output data of get_first_proxy_ip
        # doesn't work we just make sure to ecrase previous value
        try:
            presence.proxy_ip = get_first_proxy_ip(request)
        except:
            presence.proxy_ip = None
    else:
        # this is important to set it to None to ecrase any previous
        # potential value
        presence.proxy_ip = None

    presence.save()

    response_serializer = PresenceSerializer(presence)
    if created:
        status = HTTP_201_CREATED
    else:
        status = HTTP_200_OK

    return Response(response_serializer.data, status=status)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def away(request, *args, **kwargs):
    """
    === Set user away status ===

    You can provide this field in POST parameters or have a default value :
      * status : true or false (default is true)
    """

    away_serializer = AwaySerializer(data=request.data)
    away_serializer.is_valid(raise_exception=True)

    presence, created = Presence.objects.get_or_create(
        user=request.user)
    presence.away = away_serializer.data['status']
    presence.save()

    response_serializer = PresenceSerializer(presence)
    if created:
        status = HTTP_201_CREATED
    else:
        status = HTTP_200_OK

    return Response(response_serializer.data, status=status)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def toggle_away(request, *args, **kwargs):
    """
    === Change an user away status ===
    """

    presence, created = Presence.objects.get_or_create(
        user=request.user)
    presence.away = not presence.away
    presence.save()

    response_serializer = PresenceSerializer(presence)
    if created:
        status = HTTP_201_CREATED
    else:
        status = HTTP_200_OK

    return Response(response_serializer.data, status=status)


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
