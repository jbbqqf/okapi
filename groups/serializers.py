# -*- coding: utf-8 -*-

from rest_framework import serializers
from groups.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'url', 'ml', 'description', 'left', 'right')
