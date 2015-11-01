# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import (
    ModelSerializer, Serializer, IntegerField, ChoiceField, ValidationError)

from chat.models import Channel, Post
from profiles.models import User
from groups.models import Group


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'public', 'active', 'created', ]


class ChannelMemberSerializer(Serializer):
    PERMISSIONS = [
        ('read_channel', 'Read Channel'),
        ('write_channel', 'Write Channel'),
        ('admin_channel', 'Admin Channel'),
    ]
    user = IntegerField()
    permissions = ChoiceField(PERMISSIONS)

    def validate_user(self, value):
        try:
            User.objects.get(id=value)
            return value

        except ObjectDoesNotExist:
            raise ValidationError(
                'User id ({}) does not match any user'.format(value))


class ChannelGroupSerializer(Serializer):
    PERMISSIONS = [
        ('read_channel', 'Read Channel'),
        ('write_channel', 'Write Channel'),
        ('admin_channel', 'Admin Channel'),
    ]
    group = IntegerField()
    permissions = ChoiceField(PERMISSIONS)

    def validate_group(self, value):
        try:
            Group.objects.get(id=value)
            return value

        except ObjectDoesNotExist:
            raise ValidationError(
                'Group id ({}) does not match any group'.format(value))


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = ['author', 'type', ]
