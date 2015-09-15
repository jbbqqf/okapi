from django.db import models
from django.forms import ModelForm
from users.models import User

class Group(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    mailing = models.CharField(max_length=100)
    description = models.TextField()
    parent_id = models.IntegerField()

    def __unicode__(self):
        return self.name

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'url', 'mailing', 'description', 'parent_id']

class GroupUser(models.Model):
    ROLES = [
        ('u', 'user'),
        ('a', 'admin'),
    ]

    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    role = models.CharField(max_length=1, choices=ROLES)

    class Meta:
        unique_together = (('user', 'group'),)

class GroupUserForm(ModelForm):
    class Meta:
        model = GroupUser
        fields = ['user', 'group', 'role']
