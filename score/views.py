# -*- coding: utf-8 -*-

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import (
    authentication_classes, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.filters import DjangoFilterBackend

from score.pagination import ScoresPagination
from score.filters import ScoreFilter, CurrentScoreFilter
from score.models import Score, CurrentScore
from score.serializers import ScoreSerializer, CurrentScoreSerializer


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
class ScoreView(ReadOnlyModelViewSet):
    """
    === All discrete differential values refering to date, user and game ===

    Instead of recording a single score value for each user, it allows
    flexibility to display score tables that can be filtered for a particular
    game and/or between two dates.

    For exemple, we can imagine a monthly score table only for button players.
    """

    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ScoreFilter
    pagination_class = ScoresPagination


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
class CurrentScoreView(ReadOnlyModelViewSet):
    """
    === A single value per user easy to show ===

    Instead of having to compute over a large amount of score entries to
    retrieve the main scores, you should use this score per default.
    """

    queryset = CurrentScore.objects.all()
    serializer_class = CurrentScoreSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CurrentScoreFilter
