from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Group(models.Model):
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
