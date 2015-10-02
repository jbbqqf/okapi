from os.path import join, isdir
from os import makedirs, rename
from shutil import move

from django.db import transaction
from django.shortcuts import render
from django.conf import settings

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from fileshare.models import File, Directory
from fileshare.serializers import FileSerializer, DirectorySerializer
from fileshare.filters import FileFilter, DirectoryFilter
from common.common import cmd

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.filter(deleted=False)
    serializer_class = FileSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    filter_class = FileFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class DirectoryViewSet(viewsets.GenericViewSet,
                       ListModelMixin,
                       RetrieveModelMixin):
    queryset = Directory.objects.filter(deleted=False)
    serializer_class = DirectorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    filter_class = DirectoryFilter

    def create(self, request, pk=None):
        serializer = DirectorySerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    new_dir = serializer.save()
                    makedirs(join(settings.MEDIA_ROOT,
                                  'fileshare',
                                  new_dir.to_relative()))
            except OSError as e:
                error = {'message': 'Server could not create directory'}
                return Response(error,
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        src_dir = self.get_object()
        src_path = src_dir.to_relative()
        serializer = DirectorySerializer(src_dir, data=request.data)
        
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                dest_path = serializer.save().to_relative()
                parent_path = src_dir.parent.to_relative()

                # FileShare Root
                fsr = join(settings.MEDIA_ROOT, 'fileshare')
                if not isdir(join(fsr, parent_path)):
                    makedirs(join(fsr, parent_path))
                
                abs_src = join(fsr, src_path)
                abs_dest = join(fsr, dest_path)

                cmd('mv', abs_src, abs_dest)

        except OSError as e:
            error = {'message': 'Server could not create directory'}
            return Response(error,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data)
