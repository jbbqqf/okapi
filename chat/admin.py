# -*- coding: utf-8 -*-

from django.contrib import admin
from chat.models import Channel, ChannelForm, Post, PostForm


class ChannelAdmin(admin.ModelAdmin):
    form = ChannelForm
    list_display = ('id', 'name', 'public', 'active', 'created',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('channel', 'date', 'author', 'type', 'content',)
    search_fields = ('channel', 'author', 'content',)

admin.site.register(Channel, ChannelAdmin)
admin.site.register(Post, PostAdmin)
