from django.db import models
from django.forms import ModelForm

from django.contrib.auth.models import User

from profiles.models import User

class Channel(models.Model):
    """
    One major criticism of karibou was the single chat instance. People could
    not have private conversations in groups. This Channel model allows not
    only this but could also replace flashmails.

    All promos and all clubs should have their default channel, and a super
    default channel should always be available for everyone.
    """

    name = models.CharField(max_length=32, unique=True)
    public = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

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
        fields = ['name', 'public',]

class Post(models.Model):
    """
    Posts are lines of channels.

    Connected users should be able to send only `m` posts from the user
    interface. For any other kind of post that could be displayed to users,
    only backend through application requests should be allowed create those.
    """

    TYPE = [
        ('m', 'message'),
        ('s', 'score'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    type = models.CharField(max_length=1, choices=TYPE, default=TYPE[0][0])
    content = models.CharField(max_length=512)
    channel = models.ForeignKey(Channel)

    def __unicode__(self):
        return u'[{}] {}: {}'.format(self.channel, self.author, self.content)

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type', 'content', 'channel',]
