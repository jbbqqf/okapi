# -*- coding: utf-8 -*-

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import (
    authentication_classes, permission_classes, api_view)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response

from common.pagination import GamePagination
from score.filters import ScoreFilter, CurrentScoreFilter
from score.models import Score, CurrentScore
from score.serializers import (
    StatsSerializer, StatsResponseSerializer, MyStatsSerializer,
    MyStatsResponseSerializer, ScoreSerializer, CurrentScoreSerializer)
from score.utils import get_bounded_scores, get_players_scores


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def stats(request):
    """
    === Provide some customizable stats about scores ===

    You can send any number of those fields in JSON. If one of those field
    is not sent, it will take its default value :
      * game : 'p', 'd', 't', 'b', etc. or '*' for all games (default is '*')
      * top : Integer for the maximum number of players you want to have
              informations about (response can contain less if there are not
              enough users having Score entries). (default is 10, min is 1)
      * reverse : true or false (default is false). Instead of returning the
                  first <top> players, it returns the last <top>.
      * start : datetime setting a greater or equal boundary (default is null :
                considering scores since the firsts)
      * end : datetime setting a lower or equal boundary (default is null :
              considering scores until the latests)

    The response will contain a sorted list of those fields :
      * player : user id as int
      * score : player score as int
    """

    stats_serializer = StatsSerializer(data=request.data)
    stats_serializer.is_valid(raise_exception=True)

    game = stats_serializer.data['game']
    start = stats_serializer.data['start']
    end = stats_serializer.data['end']

    queryset = get_bounded_scores(game=game, start=start, end=end)

    reverse = stats_serializer.data['reverse']
    players_scores, sorted_players = get_players_scores(queryset=queryset,
                                                        reverse=reverse)

    top_x = stats_serializer.data['top']
    players_count = len(sorted_players)
    if top_x > players_count:
        top_x = players_count

    considered_scores = []
    for x in range(top_x):
        player = sorted_players[x]
        score = players_scores[player]
        considered_scores.append({'player': player.id,
                                  'score': score})

    response_serializer = StatsResponseSerializer(data=considered_scores,
                                                  many=True)
    response_serializer.is_valid(raise_exception=True)

    return Response(response_serializer.data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def mystats(request):
    """
    === Provide some customizable stats about requesting user score ===

    You can send any number of those fields in JSON. If one of those field
    is not sent, it will take its default value :
      * game : 'p', 'd', 't', 'b', etc. or '*' for all games (default is '*')
      * start : datetime setting a greater or equal boundary (default is null :
                considering scores since the firsts)
      * end : datetime setting a lower or equal boundary (default is null :
              considering scores until the latests)

    The response will contain those fields :
      * my_score : user score for considered game(s) as int
      * my_rank : user ranking as int
      * my_reverse_rank : players_count - my_rank + 1 as int
      * players_count : number of players having at least one Score entry as
                        int
    """

    my_stats_serializer = MyStatsSerializer(data=request.data)
    my_stats_serializer.is_valid(raise_exception=True)

    game = my_stats_serializer.data['game']
    start = my_stats_serializer.data['start']
    end = my_stats_serializer.data['end']

    queryset = get_bounded_scores(game=game, start=start, end=end)

    players_scores, sorted_players = get_players_scores(queryset=queryset)

    sorted_players = sorted(players_scores)
    players_count = len(sorted_players)

    me = request.user
    my_rank = 0
    for player in sorted_players:
        my_rank += 1
        if player == me:
            my_reverse_rank = players_count - my_rank + 1
            break
    else:
        my_rank = 0
        my_reverse_rank = 0

    my_stats = {
        'my_score': players_scores.get(me, default=0),
        'my_rank': my_rank,
        'my_reverse_rank': my_reverse_rank,
        'players_count': players_count,
    }

    response_serializer = MyStatsResponseSerializer(data=my_stats)
    response_serializer.is_valid(raise_exception=True)

    return Response(response_serializer.data)


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
    pagination_class = GamePagination


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
