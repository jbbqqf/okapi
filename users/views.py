from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from groups.serializers import GroupSerializer
from users.serializers import UserSerializer
from groups.models import Group, GroupUser
from users.models import User

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route()
    def groups(self, request, pk=None):
        user = self.get_object()
        group_users = GroupUser.objects.filter(user=user.id)

        groups = []
        for group_user in group_users:
             groups.append(Group.objects.get(id=group_user.group.id))
 
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
