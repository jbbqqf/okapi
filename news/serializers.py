# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer
from news.models import Event


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        read_only_fields = ['author', 'created', ]
        fields = ['id', 'author', 'title', 'description', 'link',
                  'created', 'dday', ]
