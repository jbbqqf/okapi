# -*- coding: utf-8 -*-

from score.models import Score


def get_bounded_scores(game='*', start=None, end=None):
    if game == '*':
        queryset = Score.objects.all()
    else:
        queryset = Score.objects.filter(game=game)

    if start is not None:
        queryset.filter(date__gte=start)

    if end is not None:
        queryset.filter(date__lte=end)

    return queryset


def get_players_scores(queryset=None, reverse=False):
    if queryset is None:
        queryset = Score.objects.all()

    players_scores = {}
    for score in queryset:
        if score.user not in players_scores:
            players_scores[score.user] = 0
        players_scores[score.user] += score.value

    sorted_players = sorted(players_scores, reverse=reverse)

    return players_scores, sorted_players
