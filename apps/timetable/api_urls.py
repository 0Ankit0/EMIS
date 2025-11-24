"""API URLs for timetable app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'academic-years', api_views.AcademicYearViewSet, basename='academic-year')
router.register(r'semesters', api_views.SemesterViewSet, basename='semester')
router.register(r'timeslots', api_views.TimeSlotViewSet, basename='timeslot')
router.register(r'rooms', api_views.RoomViewSet, basename='room')
router.register(r'entries', api_views.TimetableEntryViewSet, basename='entry')
router.register(r'exceptions', api_views.TimetableExceptionViewSet, basename='exception')

urlpatterns = router.urls
