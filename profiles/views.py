from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets

from profiles.models import Profile
from profiles.serializers import ProfileSerializer, UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
