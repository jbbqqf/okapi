# -*- coding: utf-8 -*-

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import (
    api_view, list_route, authentication_classes, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from common.pagination import GamePagination
from button.filters import ClearFilter
from button.models import Clear
from button.serializers import ClearSerializer


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def clear(request):
    """
    === Clear the button ! ===

    Once per hour maximum.
    """

    clear = Clear(user=request.user)
    clear.save()

    serializer = ClearSerializer(clear)
    return Response(serializer.data, status=HTTP_201_CREATED)


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
