# -*- coding: utf-8 -*-

from rest_framework import serializers
from groups.models import Group, GroupUser, okaGroup

class okaGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'url', 'mailing', 'description', 'parent',]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'url', 'mailing', 'description', 'parent')

class GroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUser
        fields = ('user', 'group', 'role')
