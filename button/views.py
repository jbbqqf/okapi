# -*- coding: utf-8 -*-

from datetime import timedelta

from django.db import DataError
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import (
    api_view, list_route, authentication_classes, permission_classes,
    throttle_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from rest_framework.throttling import UserRateThrottle

from common.pagination import GamePagination
from button.filters import ClearFilter
from button.models import Clear
from score.models import Score
from button.serializers import ClearSerializer, MyStatsSerializer


class OncePerHourUserThrottle(UserRateThrottle):
    rate = '1/hour'


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
@throttle_classes((OncePerHourUserThrottle,))
def clear(request):
    """
    === Clear the button ! ===

    Once per hour maximum.
    """

    clear = Clear(user=request.user)
    try:
        clear.save()

    except DataError:
        error = {'message': 'You cannot clear two times in a row !'}
        return Response(error, status=HTTP_409_CONFLICT)

    serializer = ClearSerializer(clear)
    return Response(serializer.data, status=HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def mystats(request):
    """
    === Provide some personnal stats about your participation ===
    """

    my_button_scores = Score.objects.filter(user=request.user, game='b')

    my_score = 0
    for score in my_button_scores:
        my_score += score.value

    my_best_score = my_button_scores.order_by('value')[0]
    my_best_conquest = timedelta(seconds=(my_best_score.value / 10))

    my_clicks = my_button_scores.count()

    serializer = MyStatsSerializer(data={'my_score': my_score,
                                         'my_best_conquest': my_best_conquest,
                                         'my_clicks': my_clicks,
                                         })
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)


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
