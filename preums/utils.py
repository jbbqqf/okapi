# -*- coding: utf-8 -*-

from datetime import datetime
from pytz import timezone

from chat.models import Channel, Post
from score.models import Score


def is_posted_today(string, date, channel=None, excluded_players=[]):
    if channel is None:
        # if no channel is specified we assume it's the general channel
        channel = Channel.objects.get(id=1)

    # TODO: check if this is really UTC we want here
    paris_tz = timezone('UTC')
    post_day = paris_tz.localize(datetime(date.year,
                                          date.month,
                                          date.day))

    matching_posts_so_far = Post.objects.filter(channel=channel,
                                                type='m',
                                                date__gte=post_day,
                                                date__lte=date,
                                                content=string)

    for player in excluded_players:
        matching_posts_so_far = matching_posts_so_far.exclude(author=player)

    if not matching_posts_so_far.exists():
        return None

    matching_posts_so_far.order_by('date')
    return matching_posts_so_far[0]


def is_preums(post):
    if is_posted_today('preums', post.date) == post:
        score = Score(user=post.author, game='p', value=500000)
        score.save()


def is_deuz(post):
    preums = is_posted_today('preums', post.date)
    if preums is not None:
        deuz = is_posted_today('deuz',
                               post.date,
                               excluded_players=[preums.author])
        if deuz == post:
            if preums.author != post.author:
                score = Score(user=post.author, game='d', value=300000)
                score.save()


def is_troiz(post):
    preums = is_posted_today('preums', post.date)
    if preums is not None:
        deuz = is_posted_today('deuz',
                               post.date,
                               excluded_players=[preums.author])
        if deuz is not None:
            troiz = is_posted_today('troiz',
                                    post.date,
                                    excluded_players=[preums.author,
                                                      deuz.author])
            if troiz == post:
                if post.author not in [preums.author, deuz.author]:
                    score = Score(user=post.author, game='t', value=100000)
                    score.save()


def is_dernz(post):
    general_channel = Channel.objects.get(id=1)

    paris_tz = timezone('UTC')
    post_day = paris_tz.localize(datetime(post.date.year,
                                          post.date.month,
                                          post.date.day))

    latests_dernz = Post.objects.filter(channel=general_channel,
                                        type='m',
                                        date__gte=post_day,
                                        date__lte=post.date,
                                        content='dernz')

    user_latests_dernz = latests_dernz.filter(author=post.author)

    # if there is exactly one it's the first one
    if user_latests_dernz.count() == 1:
        latests_dernz = latests_dernz.exclude(author=post.author)

        if latests_dernz.exists():
            latest_dernz = latests_dernz.order_by('-date')[0]

            score = Score(user=latest_dernz.author, game='n', value=-300000)
            score.save()

        score = Score(user=post.author, game='n', value=300000)
        score.save()
