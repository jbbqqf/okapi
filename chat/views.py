from django.shortcuts import render

from rest_framework import viewsets

from chat.serializers import PostSerializer
from chat.models import Post

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
