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
    """
    === Directory objects map system directories for fileshare application ===

    Directories support only alphanumeric characters and ` `, `_` and `-` (even
    if posix norm allows you some special characters).

    Since directories are stored in filesystem, you cannot have two directories
    with the same name on the same line level.

    If provided values are validated and Directory is created/updated/deleted in
    database, a request is sent to the system to update the system directory. If
    the system encounters a problem (corrupted filesystem, bad permissions...),
    a rollback will be processed for the last database insertion and an error
    500 will be returned.
    """

    queryset = Directory.objects.filter(deleted=False)
    serializer_class = DirectorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    filter_class = DirectoryFilter

    # FileShare application system Root directory
    fsr = join(settings.MEDIA_ROOT, 'fileshare')

    def create(self, request, pk=None):
        """
        Request for creating a fileshare directory.

        You cannot create a directory whose parent is null, since only already
        existing root directory is allowed to have a null parent.
        """
        
        serializer = DirectorySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                new_dir = serializer.save()
                # makedirs create all parent directories if they are missing
                # in case of a corupted filesystem for exemple
                makedirs(join(self.fsr, new_dir.to_relative()))

        except OSError as e:
            error = {'message': 'Server could not create directory'}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Request for updating a fileshare directory.

        You cannot update a directory to a null parent, since only already
        existing root directory is allowed to have a null parent.
        """

        # TODO: retourner une erreur dans le cas ou on deplace le parent
        #       dans un child

        dir = self.get_object()
        serializer = DirectorySerializer(dir, data=request.data)
        
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                dest_dir = serializer.save()
                parent_path = dir.parent.to_relative()

                # makedirs create all parent directories if they are missing
                # in case of a corupted filesystem for exemple
                if not isdir(join(self.fsr, parent_path)):
                    makedirs(join(self.fsr, parent_path))
                
                abs_src = join(self.fsr, dir.to_relative())
                abs_dest = join(self.fsr, dest_dir.to_relative())

                # Here we don't use os.path and shutil rename/mv builtin
                # functions since we cannot change name and parent
                # simultaneously. There is a small risk of collision if you
                # rename a directory with a name that already exists in current
                # location, and an other risk if you first want to move your
                # directory without renaming it. That's why we use a custom cmd
                # function which emulates a shell command.
                cmd('mv', abs_src, abs_dest)

        except OSError as e:
            error = {'message': 'Server could not create directory'}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Request for deleting a directory.

        There is no particular permissions to delete directories. Any logged
        user can do it but only if it's empty. If it's not, an error 400 will be
        returned. Only creators and admins can delete contained files. Root
        directory (which parent is null) is an exception that can never be
        deleted.
        """

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

        # I don't know if it's possible to reach those lines but just in case...
        error = {'message': 'Unknown server error. Please report to an admin.'}
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
