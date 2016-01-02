# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer
from button.models import Clear


class ClearSerializer(ModelSerializer):
    class Meta:
        model = Clear
        read_only_fields = ('id', 'user', 'date',)
