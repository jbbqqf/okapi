# -*- coding: utf-8 -*-

from rest_framework.serializers import (
    ModelSerializer, Serializer, CharField, DateTimeField, BooleanField,
    IntegerField)
from score.models import Score, CurrentScore


class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        read_only_fields = ('user', 'game', 'value', 'date',)


class CurrentScoreSerializer(ModelSerializer):
    class Meta:
        model = CurrentScore
        read_only_fields = ('user', 'value',)


class StatsSerializer(Serializer):
    game = CharField(default='*')
    # TODO: validate top is >= 0
    top = IntegerField(default=10)
    reverse = BooleanField(default=False)
    start = DateTimeField(default=None)
    end = DateTimeField(default=None)


class StatsResponseSerializer(Serializer):
    player = IntegerField()
    score = IntegerField()


class MyStatsSerializer(Serializer):
    game = CharField(default='*')
    start = DateTimeField(default=None)
    end = DateTimeField(default=None)


class MyStatsResponseSerializer(Serializer):
    my_score = IntegerField()
    my_rank = IntegerField()
    my_reverse_rank = IntegerField()
    players_count = IntegerField()
