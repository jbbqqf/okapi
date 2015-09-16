# -*- coding: utf-8 -*-

from rest_framework import serializers
from chat.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
