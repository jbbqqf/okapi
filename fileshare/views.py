from os.path import join, isdir
from os import makedirs, rmdir

from django.db import transaction
from django.shortcuts import render
from django.conf import settings

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from fileshare.models import File, Directory
from fileshare.serializers import FileSerializer, DirectorySerializer
from fileshare.permissions import IsFileOwnerOrAdminOrReadOnly
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

@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly,))
class DirectoryViewSet(viewsets.GenericViewSet,
                       ListModelMixin,
                       RetrieveModelMixin):
    queryset = Directory.objects.filter(deleted=False)
    serializer_class = DirectorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    filter_class = DirectoryFilter

    # FileShare application system Root directory
    fsr = join(settings.MEDIA_ROOT, 'fileshare')

    def create(self, request, pk=None):
        serializer = DirectorySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                new_dir = serializer.save()
                makedirs(join(self.fsr, new_dir.to_relative()))

        except OSError as e:
            error = {'message': 'Server could not create directory'}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data)

    def update(self, request, pk=None):
        dir = self.get_object()
        serializer = DirectorySerializer(dir, data=request.data)
        
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                dest_dir = serializer.save()
                parent_path = dir.parent.to_relative()

                if not isdir(join(self.fsr, parent_path)):
                    makedirs(join(self.fsr, parent_path))
                
                abs_src = join(self.fsr, dir.to_relative())
                abs_dest = join(self.fsr, dest_dir.to_relative())

                cmd('mv', abs_src, abs_dest)

        except OSError as e:
            error = {'message': 'Server could not create directory'}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        dir = self.get_object()

        if dir.parent is None:
            error = {'message': 'Don\'t DELETE root directory you hacker :o'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        dir_childs = Directory.objects.filter(parent=dir).exists()
        file_childs = File.objects.filter(parent=dir).exists()

        if (dir_childs or file_childs) is True:
            error = {'message': 'Cannot DELETE a directory which has childs'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                dir.delete()
                rmdir(join(self.fsr, dir.to_relative()))
                return Response(status=status.HTTP_204_NO_CONTENT)

        except OSError as e:
            msg = 'Could not remove directory{}'.format(dir.to_absolute())
            error = {'message': msg}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        error = {'message': 'Unknown server error. Please report to an admin.'}
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
