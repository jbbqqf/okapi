from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Group(models.Model):
    """
    Lots of use can be pictured for groups, even if the first goal here is to
    regroup people by promotion and by club affinity.

    An important thing to notice here is the parent field. Django's ForeignKey
    constraints do not allow such a field to be empty. Each group should have a
    parent event if it's not relevant (i.e. top-level groups such as `Fi`). For
    this reason, a virtual root group should be maintained.
    """

    name = models.CharField(max_length=30)
    url = models.CharField(max_length=100, blank=True)
    mailing = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self')

    def __unicode__(self):
        return self.name

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'url', 'mailing', 'description', 'parent']

class GroupUser(models.Model):
    """
    This model could be a manytomany field in Group. But since we're working
    with a rest API it would be less convenient when requesting.
    """

    ROLES = [
        ('u', 'user'),
        ('a', 'admin'),
    ]

    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    role = models.CharField(max_length=1, choices=ROLES, default=ROLES[0][0])

    class Meta:
        unique_together = (('user', 'group'),)

    def __unicode__(self):
        role = 'unknown role'
        for role_stored, role_title in self.ROLES:
            if role_stored == self.role:
                role = role_title
        return u'{} is {} in {}'.format(self.user, role, self.group)

class GroupUserForm(ModelForm):
    class Meta:
        model = GroupUser
        fields = ['user', 'group', 'role']


def get_group_members(group):
    """
    Search in manytomany relationship GroupUser model for users belonging to
    a group given as argument. Return a list of users or an empty list.
    """

    matches = GroupUser.objects.filter(group=group)
    members = [member.user for member in matches]
    return members


def get_user_groups(user):
    """
    Search in manytomany relationship GroupUser model for groups a user given
    as argument belongs to. Return a list of groups or an empty list.
    """

    matches = GroupUser.objects.filter(user=user)
    groups = [match.group for match in matches]
    return groups
