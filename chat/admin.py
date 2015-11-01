# -*- coding: utf-8 -*-

from django.contrib.admin import ModelAdmin
from django.contrib.admin.site import register
from chat.models import Channel, ChannelForm, Post, PostForm


class ChannelAdmin(ModelAdmin):
    form = ChannelForm
    list_display = ['id', 'name', 'public', 'active', 'created', ]
    search_fields = ['name', ]


class PostAdmin(ModelAdmin):
    form = PostForm
    list_display = ['channel', 'date', 'author', 'type', 'content', ]
    search_fields = ['channel', 'author', 'content', ]

register(Channel, ChannelAdmin)
register(Post, PostAdmin)
