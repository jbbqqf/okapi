from rest_framework import serializers
from news.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        read_only_fields = ['author', 'created',]
        fields = ['id', 'author', 'title', 'description', 'link',
                  'created', 'dday',]
