# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer
from online.models import Presence


class PresenceSerializer(ModelSerializer):
    class Meta:
        model = Presence
        fields = (
            'user',
            'last_passive',
            'last_active',
            'ip',
            'proxy_ip',
            'away',
        )
