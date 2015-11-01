# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer
from preferences.models import UserInterface, UserPref


class UserInterfaceSerializer(ModelSerializer):
    class Meta:
        model = UserInterface
        read_only_fields = ['name', 'comment', ]


class UserPrefSerializer(ModelSerializer):
    class Meta:
        model = UserPref
        read_only_fields = ['user', ]
        fields = ['id', 'user', 'ui', 'conf', ]
