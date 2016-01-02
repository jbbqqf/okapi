# -*- coding: utf-8 -*-

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import (
    list_route, authentication_classes, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response

from common.pagination import GamePagination
from button.filters import ClearFilter
from button.models import Clear
from button.serializers import ClearSerializer


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
class ClearView(ReadOnlyModelViewSet):
    """
    === Check who clicked when ! ===
    """

    queryset = Clear.objects.all()
    serializer_class = ClearSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ClearFilter
    pagination_class = GamePagination

    @list_route(methods=['GET'])
    def latest(self, request, *args, **kwargs):
        """
        === The latest clear ===
        """

        latest = Clear.objects.latest('date')
        serializer = self.get_serializer(latest)
        return Response(serializer.data)
