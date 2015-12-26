# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer
from groups.models import Group


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'url', 'mailing', 'description', 'parent',)
