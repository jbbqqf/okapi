# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer
from library.models import PressReview


class PressReviewSerializer(ModelSerializer):
    class Meta:
        model = PressReview
        fields = ('id', 'date', 'link',)
