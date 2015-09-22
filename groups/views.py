from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import detail_route, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.filters import DjangoFilterBackend, SearchFilter

from common.permissions import IsAdminOrReadOnly
from groups.serializers import GroupSerializer, GroupUserSerializer
from profiles.serializers import UserSerializer
from groups.models import Group, GroupUser
from groups.filters import GroupFilter

@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAdminOrReadOnly,))
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ['name', 'url', 'mailing', 'description']
    filter_class = GroupFilter

    @detail_route()
    def users(self, request, pk=None):
        group = self.get_object()
        group_users = GroupUser.objects.filter(group=group.id)

        users = []
        for group_user in group_users:
            users.append(User.objects.get(id=group_user.user.id))

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAdminOrReadOnly,))
class GroupUserViewSet(viewsets.ModelViewSet):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserSerializer
    http_method_names = ['get', 'post', 'delete', 'head', 'options',]
