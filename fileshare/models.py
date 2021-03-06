# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.contrib.auth.models import User

ALPHANUMERIC = RegexValidator(r'^[0-9a-zA-Z. _-]*$',
                              'Use only alphanumeric characters or `. _-`.')


class Directory(models.Model):
    """
    Directories in fileshare application aim to map system directories in base
    to be able to reference files and subdirectories as their parent.

    Directories support only alphanumeric characters and `.`, ` `, `_` and `-`
    (even if posix norm allows some special characters). This directory model
    does not record the owner of a directory, allowing everyone to edit them.
    However API views do not allow you to remove a directory if it's not empty,
    and Files are subject to write rights.

    Root directory is recorded in base but should NEVER be edited unless you
    know what you're doing, even if it's possible through admin interface. It
    cannot be edited through API interface.
    """

    # null is allowed only for root directory
    parent = models.ForeignKey('self', null=True)
    name = models.CharField(max_length=32, validators=[ALPHANUMERIC])
    # deleted is not yet implemented but it should allow users to remove a
    # ressource without being destroyed on server (trashbin functionnality ?)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.to_absolute()

    def get_path_ids(self):
        """
        Return directory path as a list of parent ids. Root directory is
        always considered to have an id equal to 1. The first directory to
        call this method IS part of the list.
        """

        if self.parent is None:
            return [1]

        else:
            path = [self.id]
            return self.parent.get_path_ids() + path

    def to_absolute(self):
        """
        Return directory path from `~okapi/www/media/fileshare` with a trailing
        slash. It's an `absolute` name because a initial slash is added too.
        exemple : `/pokedex/lightning/pikachu/`
        """

        if self.parent is None:
            return '/'
        else:
            return '{}{}/'.format(self.parent.to_absolute(), self.name)

    def to_relative(self):
        """
        Return directory path from `~okapi/www/media/fileshare` with a trailing
        slash. It's an `relative` name because a initial slash is added too. It
        should be prefered to self.to_absolute when you need to concatenate the
        directory path with something else (i.e. os.path.join).
        exemple : `pokedex/lightning/pikachu/`
        """

        if self.parent is None:
            return ''
        else:
            return '{}{}/'.format(self.parent.to_relative(), self.name)

    def is_parent(self, dir):
        """
        Check (recursively) if self is parent of supplied `dir` (supply a
        simple name). Return True or False.
        This method should be used before making operations on a directory such
        as changing its location (ie. if a user requests to move a parent in
        one of its child dir).
        """

        childs = Directory.objects.filter(parent=self)

        if dir in childs:
            return True

        elif childs.exists():
            for child in childs:
                if child.is_parent(dir):
                    return True

        else:
            return False


class DirectoryForm(ModelForm):
    class Meta:
        model = Directory
        fields = ('name', 'parent', 'deleted',)


class File(models.Model):
    """
    Files in fileshare application map system stored files in media/files

    File names support only alphanumeric characters and `.`, ` `, `_` and `-`
    (even if posix norm allows some special characters). This File model does
    record the creator of a directory, which also becomes its owner. Only
    owners and admins are able to PUT or DELETE a File.
    """

    # use null only if your file if stored in the root directoy
    parent = models.ForeignKey(Directory, null=True)
    name = models.CharField(max_length=32, validators=[ALPHANUMERIC])
    file = models.FileField(upload_to='files')
    creator = models.ForeignKey(User)
    # deleted is not yet implemented but it should allow users to remove a
    # ressource without being destroyed on server (trashbin functionnality ?)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_path_ids(self):
        """
        Return file path as a list of parent ids. Root directory is
        always considered to have an id equal to 1. This File id is NOT part
        of the list.
        """

        return self.parent.get_path_ids()

    def __unicode__(self):
        return '{}{}'.format(self.parent, self.name)


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ('name', 'parent', 'file', 'creator', 'deleted',)
