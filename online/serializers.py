# -*- coding: utf-8 -*-

from rest_framework.serializers import (
    ModelSerializer, Serializer, BooleanField)
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


class IPPrivacySerializer(Serializer):
    """
    This serializer allows a user notifying his/her presence to tell the
    backend not to save his/her ip.

    Note that the two default=True clauses allows a user to not send any json
    at all.
    """

    show_ip = BooleanField(default=True)
    show_proxy_ip = BooleanField(default=True)


class AwaySerializer(Serializer):
    """
    A one field serializer allowing a user to set his/her away status.

    Note that the default=True clause allows a user to not send any json at
    all.
    """

    status = BooleanField(default=True)
