# -*- coding: utf-8 -*-

from rest_framework import serializers
from fileshare.models import File, Directory

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'parent',)

class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ('id', 'name', 'parent',)

    def validate(self, data):
        # TODO: PATCH compatibility (name / parent are not mandatory)
        name = data['name']
        parent = data['parent']

        # only `/`, a static Directory, can have parent set to null
        if parent is None:
            error = {'message': 'Parent field can\'t be None'}
            raise serializers.ValidationError(error)

        # it is not allowed to have two identical names
        same_level_dirs = Directory.objects.filter(parent=parent)
        for same_level_dir in same_level_dirs:
            if same_level_dir.name == name:
                parent_name = parent.to_absolute()
                error = 'name {} already used in parent {}'.format(name,
                                                                   parent_name)
                raise serializers.ValidationError(error)
        else:
            return data
