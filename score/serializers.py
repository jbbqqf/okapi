# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer
from score.models import Score, CurrentScore


class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        read_only_fields = ('user', 'game', 'value', 'date',)


class CurrentScoreSerializer(ModelSerializer):
    class Meta:
        model = CurrentScore
        read_only_fields = ('user', 'value',)
