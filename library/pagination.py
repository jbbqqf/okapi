# -*- coding: utf-8 -*-

from rest_framework.pagination import PageNumberPagination


class PressReviewPagination(PageNumberPagination):
    page_size = 30
    page_size_query_params = 'items'
    max_page_size = 100
