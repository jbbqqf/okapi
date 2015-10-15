# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from chat.models import Channel, Post
from profiles.models import User
from groups.models import Group

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'public', 'active',]

class ChannelMemberSerializer(serializers.Serializer):
    PERMISSIONS = [
        ('read_channel', 'Read Channel'),
        ('write_channel', 'Write Channel'),
        ('admin_channel', 'Admin Channel'),
    ]
    user = serializers.IntegerField()
    permissions = serializers.ChoiceField(PERMISSIONS)

    def validate_user(self, value):
        try:
            User.objects.get(id=value)
            return value

        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'User id ({}) does not match any user'.format(value))

class ChannelGroupSerializer(serializers.Serializer):
    PERMISSIONS = [
        ('read_channel', 'Read Channel'),
        ('write_channel', 'Write Channel'),
        ('admin_channel', 'Admin Channel'),
    ]
    group = serializers.IntegerField()
    permissions = serializers.ChoiceField(PERMISSIONS)

    def validate_group(self, value):
        try:
            Group.objects.get(id=value)
            return value

        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Group id ({}) does not match any group'.format(value))

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = ['author', 'type',]
