"""Exams API Views"""
from .exam import ExamViewSet
from .exam_result import ExamResultViewSet
from .exam_schedule import ExamScheduleViewSet

__all__ = [
    'ExamViewSet',
    'ExamResultViewSet',
    'ExamScheduleViewSet',
]
