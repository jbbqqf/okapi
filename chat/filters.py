# -*- coding: utf-8 -*-

from django_filters import (FilterSet, CharFilter, DateTimeFilter,
                            NumberFilter, BooleanFilter)
from guardian.shortcuts import get_objects_for_user
from rest_framework import filters
from chat.models import Post, Channel


def get_readable_channel_ids(user):
    """
    Return a list of channel ids on which user given in parameter has at least
    read_channel permission.

    It also includes public channels, where anyone can read/write on.

    Channel ids are unique.
    """

    readable_channels = get_objects_for_user(user, 'chat.read_channel',
                                             use_groups=True)
    readable_ids = [c.id for c in readable_channels]

    public_channels = Channel.objects.filter(public=True)
    for public_channel in public_channels:
        readable_ids.append(public_channel.id)

    unique_readable_ids = set(readable_ids)

    return unique_readable_ids


class ReadableChannelFilter(filters.BaseFilterBackend):
    """
    All users cannot see what they want. They are restricted to see only
    channels on which they have at least read_channel permission.
    """

    def filter_queryset(self, request, queryset, view):
        readable_channel_ids = get_readable_channel_ids(request.user)
        return queryset.filter(id__in=readable_channel_ids)


class ChannelFilter(FilterSet):
    name = CharFilter(name='name', lookup_type='icontains',
                      label='name contain filter')
    public = BooleanFilter(name='public', label='is public ?')

    ca_label = 'filter channels created after or on provided date / time'
    created_after = DateTimeFilter(name='date', lookup_type='gte',
                                   label=ca_label)
    cb_label = 'filter channels created before or on provided date / time'
    created_before = DateTimeFilter(name='date', lookup_type='lte',
                                    label=ca_label)

    class Meta:
        model = Channel
        fields = ('name', 'public', 'created_after', 'created_before',)


class ReadablePostFilter(filters.BaseFilterBackend):
    """
    Since channels have permissions, posts posted in a channel are not visible
    for anyone. This filter makes sure only posts a user can read will be
    returned.
    """

    def filter_queryset(self, request, queryset, view):
        readable_channel_ids = get_readable_channel_ids(request.user)
        return queryset.filter(channel__in=readable_channel_ids)


class PostFilter(FilterSet):
    author = CharFilter(name='author', lookup_type='icontains',
                        label='author contain filter')
    type = CharFilter(name='type', label='filter on letter value')
    content = CharFilter(name='type', lookup_type='icontains',
                         label='content contain filter')
    channel = NumberFilter(name='channel',
                           label='filters posts sent on provided channel')
    afterid = NumberFilter(name='id', lookup_type='gt',
                           label='filter posts posted after given post id')

    dflabel = 'filter posts posted after or on provided date / time'
    datefrom = DateTimeFilter(name='date', lookup_type='gte', label=dflabel)
    dtlabel = 'filter posts posted before or on provided date / time'
    dateto = DateTimeFilter(name='date', lookup_type='lte', label=dtlabel)
    content = CharFilter(name='content', lookup_type='icontains',
                         label='content contain filter')

    class Meta:
        model = Post
        fields = ('author', 'type', 'content', 'datefrom', 'dateto',)
