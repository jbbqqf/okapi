from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from groups.serializers import GroupSerializer, GroupUserSerializer
from users.serializers import UserSerializer
from groups.models import Group, GroupUser
from users.models import User

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @detail_route()
    def users(self, request, pk=None):
        group = self.get_object()
        group_users = GroupUser.objects.filter(group=group.id)

        users = []
        for group_user in group_users:
            users.append(User.objects.get(id=group_user.user.id))

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
