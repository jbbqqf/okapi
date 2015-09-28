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
        name = data['name']
        parent = data['parent']

        same_level_dirs = Directory.objects.filter(parent=parent)
        for same_level_dir in same_level_dirs:
            if same_level_dir.name == name:
                parent_name = parent.to_absolute()
                error = 'name {} already used in parent {}'.format(name,
                                                                   parent_name)
                raise serializers.ValidationError(error)
        else:
            return data
