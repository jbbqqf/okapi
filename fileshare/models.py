from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from groups.models import Group

class File(models.Model):
    TYPE = [
        ('f', 'file'),
        ('d', 'directory'),
    ]

    parent = models.ForeignKey('self', null=True)
    name = models.CharField(max_length=32)
    creator = models.ForeignKey(User)
    ownergroup = models.ForeignKey(Group, null=True)
    type = models.CharField(max_length=1, choices=TYPE, default=TYPE[0][0])
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return name
