# -*- coding: utf-8 -*-

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import (
    authentication_classes, permission_classes, detail_route)
from rest_framework.permissions import AllowAny
from rest_framework.filters import DjangoFilterBackend

from online.filters import PresenceFilter
from online.models import Presence
from online.serializers import PresenceSerializer


@permission_classes((AllowAny,))
class PresenceView(ReadOnlyModelViewSet):
    """
    """

    queryset = Presence.objects.all()
    serializer_class = PresenceSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PresenceFilter
