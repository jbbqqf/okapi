# -*- coding: utf-8 -*-

from rest_framework.serializers import (
    ModelSerializer, Serializer, IntegerField, DurationField)
from button.models import Clear


class ClearSerializer(ModelSerializer):
    class Meta:
        model = Clear
        read_only_fields = ('id', 'user', 'date',)


class MyStatsSerializer(Serializer):
    my_score = IntegerField()
    my_best_conquest = DurationField()
    my_clicks = IntegerField()
