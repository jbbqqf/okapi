from django.shortcuts import render
from rest_framework import viewsets
from groups.serializers import GroupSerializer
from groups.models import Group

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
