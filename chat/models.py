# -*- coding: utf-8 -*-

from django.db.models import (Model, CharField, BooleanField, DateTimeField,
                              ForeignKey)
from django.forms import ModelForm
from django.contrib.auth.models import User


class Channel(Model):
    """
    One major criticism of karibou was the single chat instance. People could
    not have private conversations in groups. This Channel model allows not
    only this but could also replace flashmails.

    All promos and all clubs should have their default channel, and a super
    default channel should always be available for everyone.
    """

    name = CharField(max_length=32, unique=True)
    public = BooleanField(default=True)
    active = BooleanField(default=True)
    created = DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.public:
            visibility = 'Public'

        else:
            visibility = 'Private'

        return '{} channel `{}`'.format(visibility, self.name)

    class Meta:
        # read: you can read what people say but cannot spam them
        # write: default permission allowing to read/write on channel
        # admin: write permissions + can add/remove users/groups
        permissions = (
            ('read_channel', 'Read Channel'),
            ('write_channel', 'Write Channel'),
            ('admin_channel', 'Admin Channel'),
        )


class ChannelForm(ModelForm):
    class Meta:
        model = Channel
        fields = ('name', 'public',)


class Post(Model):
    """
    Posts are lines of channels.

    Connected users should be able to send only `m` posts from the user
    interface. For any other kind of post that could be displayed to users,
    only backend through application requests should be allowed create those.
    """

    TYPE = (
        ('m', 'message'),
        ('s', 'score'),
    )

    date = DateTimeField(auto_now_add=True)
    author = ForeignKey(User)
    type = CharField(max_length=1, choices=TYPE, default=TYPE[0][0])
    content = CharField(max_length=512)
    channel = ForeignKey(Channel)

    def save(self, *args, **kwargs):
        # only if this post does not already exists (!= updated)
        if not self.pk:
            created = True

        super(Post, self).save(*args, **kwargs)

        if created:
            if self.channel.id == 1 and self.type == 'm':
                from preums.utils import is_preums, is_deuz, is_troiz, is_dernz
                from alone.utils import is_alone
                preums_keywords = [
                    ('preums', is_preums),
                    ('deuz', is_deuz),
                    ('troiz', is_troiz),
                    ('dernz', is_dernz),
                    ('alone on karibou', is_alone),
                ]

                for keyword, function in preums_keywords:
                    if self.content == keyword:
                        function(self)

    def __unicode__(self):
        return u'[{}] {}: {}'.format(self.channel, self.author, self.content)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'type', 'content', 'channel',)
