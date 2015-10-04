from django.db import models
from django.forms import ModelForm

from django.contrib.auth.models import User

from profiles.models import User
from groups.models import Group

class Channel(models.Model):
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

class ChannelForm(ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'public',]

class ChannelMember(models.Model):
    PERMS = [
        ('r', 'read'),
        ('w', 'write'),
        ('a', 'admin'),
    ]

    user = models.ForeignKey(User)
    channel = models.ForeignKey(Channel)
    permissions = models.CharField(max_length=1, choices=PERMS,
                                   default=PERMS[1][0])

    class Meta:
        unique_together = (('user', 'channel'),)

    def __unicode__(self):
        permissions = 'unknown perm'
        for perm_stored, perm_title in self.PERMS:
            if perm_stored == self.permissions:
                permissions = perm_title
        return '{} can {} in {}'.format(self.user, permissions,
                                        self.channel)

class ChannelMemberForm(ModelForm):
    class Meta:
        model = ChannelMember
        fields = ['user', 'channel', 'permissions',]

class ChannelGroup(models.Model):
    PERMS = [
        ('r', 'read'),
        ('w', 'write'),
        ('a', 'admin'),
    ]

    group = models.ForeignKey(Group)
    channel = models.ForeignKey(Channel)
    permissions = models.CharField(max_length=1, choices=PERMS,
                                   default=PERMS[1][0])
    
    class Meta:
        unique_together = (('group', 'channel'),)

    def __unicode__(self):
        permissions = 'unknown perm'
        for perm_stored, perm_title in self.PERMS:
            if perm_stored == self.permissions:
                permissions = perm_title
        return 'Group {} can {} in {}'.format(self.group, permissions,
                                              self.channel)

class ChannelGroupForm(ModelForm):
    class Meta:
        model = ChannelGroup
        fields = ['group', 'channel', 'permissions',]

class Post(models.Model):
    """
    Basically the only thing you need for a chat application.

    Connected users should be able to send `m` posts from the user interface.
    For any other kind of post that could be displayed to users, only backend
    through application requests should be allowed create those.
    """

    TYPE = [
        ('m', 'message'),
        ('s', 'score'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    type = models.CharField(max_length=1, choices=TYPE, default=TYPE[0][0])
    content = models.CharField(max_length=512)

    def __unicode__(self):
        return u'{}: {}'.format(self.author, self.content)

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type', 'content']
