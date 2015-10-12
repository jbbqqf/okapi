from django.db import models
from django.forms import ModelForm

from django.contrib.auth.models import User

from profiles.models import User
from groups.models import Group

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
        permissions = (
            ('read_channel', 'Read Channel'),
            ('write_channel', 'Write Channel'),
            ('admin_channel', 'Admin Channel'),
        )

class ChannelForm(ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'public',]

class ChannelMember(models.Model):
    """
    It could be a manytomany field... but read groups.GroupUser for more infos.
    """

    # read: you can read what people say but cannot spam them
    # write: default permission allowing to read/write on channel
    # admin: write permissions + can add/remove users/groups
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
    """
    It could be a manytomany field... but read groups.GroupUser for more infos.
    """

    # read: all group members can read what people say but cannot spam them
    # write: default permission, all group members can read/write on channel
    # admin: write permissions + can add/remove users/groups for all group
    #        members (but you should only give users admin permissions since
    #        you don't know who will join this group)
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


def get_channel_groups(channel):
    """
    Search in manytomany relationship ChannelGroup model for groups a channel
    given as argument belongs to. Return a list of tuples with groups and their
    permissions or an empty list.
    Example: [(<Group1>, 'r'), (<Group2>, 'a')]
    """
    
    matches = ChannelGroup.objects.filter(channel=channel)

    groups = []
    for match in matches:
        groups.append((match.group, match.permissions))

    return groups


def get_channel_members(channel):
    """
    Search in manytomany relationship ChannelMember model for members a channel
    given as argument belongs to. Return a list of tuples with users and their
    permissions or an empty list.
    Example: [(<User1>, 'r'), (<User2>, 'a')]
    """
    
    matches = ChannelMember.objects.filter(channel=channel)

    users = []
    for match in matches:
        users.append((match.user, match.permissions))

    return users
