"""
Pagination serializers and utilities
"""
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict


class PageInfoSerializer(serializers.Serializer):
    """Pagination metadata"""
    count = serializers.IntegerField(help_text="Total number of items")
    next = serializers.URLField(required=False, allow_null=True, help_text="URL to next page")
    previous = serializers.URLField(required=False, allow_null=True, help_text="URL to previous page")
    page = serializers.IntegerField(required=False, help_text="Current page number")
    page_size = serializers.IntegerField(required=False, help_text="Number of items per page")
    total_pages = serializers.IntegerField(required=False, help_text="Total number of pages")


class PaginatedResponseSerializer(serializers.Serializer):
    """
    Generic paginated response wrapper
    """
    results = serializers.ListField(help_text="List of results")
    page_info = PageInfoSerializer(help_text="Pagination metadata")


class StandardPageNumberPagination(PageNumberPagination):
    """
    Standard page number pagination
    Default page size: 20
    Max page size: 100
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'page_info': OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('page', self.page.number),
                ('page_size', self.page.paginator.per_page),
                ('total_pages', self.page.paginator.num_pages),
            ])
        })


class StandardLimitOffsetPagination(LimitOffsetPagination):
    """
    Standard limit/offset pagination
    Default limit: 20
    Max limit: 100
    """
    default_limit = 20
    max_limit = 100
    
    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'page_info': OrderedDict([
                ('count', self.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('limit', self.limit),
                ('offset', self.offset),
            ])
        })
