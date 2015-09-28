from django.db import models
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.contrib.auth.models import User
from groups.models import Group

ALPHANUMERIC = RegexValidator(r'^[0-9a-zA-Z _-]*$',
                              'Use only alphanumeric characters or ` _-`.')

class Directory(models.Model):
    parent = models.ForeignKey('self', null=True)
    name = models.CharField(max_length=32, validators=[ALPHANUMERIC])
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.to_absolute()

    def to_absolute(self):
        if self.parent is None:
            return '/'
        else:
            return '{}{}/'.format(self.parent.to_absolute(), self.name)

    def to_relative(self):
        if self.parent is None:
            return ''
        else:
            return '{}{}/'.format(self.parent.to_relative(), self.name)

class DirectoryForm(ModelForm):
    class Meta:
        model = Directory
        fields = ['name', 'parent', 'deleted',]

class File(models.Model):
    parent = models.ForeignKey(Directory, null=True)
    name = models.CharField(max_length=32, validators=[ALPHANUMERIC])
    creator = models.ForeignKey(User)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{}{}'.format(self.parent, self.name)

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'parent', 'creator', 'deleted',]
