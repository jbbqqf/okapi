# -*- coding: utf-8 -*-

from rest_framework import serializers
from chat.models import Channel, Post

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'public', 'active',]

# class ChannelMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChannelMember
#         fields = ['user', 'channel', 'permissions',]
# 
# class ChannelGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChannelGroup
#         fields = ['group', 'channel', 'permissions',]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = ['author', 'type',]
