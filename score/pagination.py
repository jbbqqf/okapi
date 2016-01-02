# -*- coding: utf-8 -*-

from rest_framework.pagination import PageNumberPagination


class ScoresPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'items'
    max_page_size = 1000
