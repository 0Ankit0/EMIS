"""Admissions API"""
from .applications import ApplicationViewSet
from .merit_lists import MeritListViewSet

__all__ = ['ApplicationViewSet', 'MeritListViewSet']
