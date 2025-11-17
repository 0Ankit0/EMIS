"""Admissions serializers"""
from .application import (
    ApplicationCreateSerializer,
    ApplicationUpdateSerializer,
    ApplicationResponseSerializer,
    ApplicationStatusUpdateSerializer
)
from .merit_list import (
    MeritListCreateSerializer,
    MeritListResponseSerializer,
    MeritListDetailSerializer
)

__all__ = [
    'ApplicationCreateSerializer',
    'ApplicationUpdateSerializer',
    'ApplicationResponseSerializer',
    'ApplicationStatusUpdateSerializer',
    'MeritListCreateSerializer',
    'MeritListResponseSerializer',
    'MeritListDetailSerializer',
]
