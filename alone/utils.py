# -*- coding: utf-8 -*-

from datetime import timedelta

from chat.models import Channel, Post
from score.models import Score


def is_alone(post):
    general_channel = Channel.objects.get(id=1)

    one_hour_ago = post.date - timedelta(hours=1)

    user_latests_alone = Post.objects.filter(channel=general_channel,
                                             type='m',
                                             date__gte=one_hour_ago,
                                             date__lt=post.date,
                                             content='alone on karibou',
                                             author=post.author)

    if not user_latests_alone.exists():
        score = Score(user=post.author, game='a', value=300000)
        score.save()
