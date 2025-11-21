"""HR API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'departments', api_views.DepartmentViewSet, basename='department')
router.register(r'designations', api_views.DesignationViewSet, basename='designation')
router.register(r'employees', api_views.EmployeeViewSet, basename='employee')
router.register(r'attendance', api_views.AttendanceViewSet, basename='attendance')
router.register(r'leaves', api_views.LeaveViewSet, basename='leave')
router.register(r'payrolls', api_views.PayrollViewSet, basename='payroll')
router.register(r'job-postings', api_views.JobPostingViewSet, basename='job-posting')
router.register(r'applications', api_views.JobApplicationViewSet, basename='application')
router.register(r'reviews', api_views.PerformanceReviewViewSet, basename='review')
router.register(r'trainings', api_views.TrainingViewSet, basename='training')
router.register(r'participants', api_views.TrainingParticipantViewSet, basename='participant')

urlpatterns = [path('', include(router.urls))]
