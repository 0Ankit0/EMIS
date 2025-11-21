"""Main URL configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/v1/', include('apps.core.api_urls')),
    
    # OpenAPI/Swagger documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Frontend URLs
    path('', include('apps.core.urls')),
    path('auth/', include('apps.authentication.urls')),
    
    # Module URLs
    path('students/', include('apps.students.urls')),
    path('admissions/', include('apps.admissions.urls')),
    path('courses/', include('apps.courses.urls')),
    path('finance/', include('apps.finance.urls')),
    path('exams/', include('apps.exams.urls')),
    path('faculty/', include('apps.faculty.urls')),
    path('library/', include('apps.library.urls')),
    path('hr/', include('apps.hr.urls')),
    path('hostel/', include('apps.hostel.urls')),
    path('transport/', include('apps.transport.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('timetable/', include('apps.timetable.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('lms/', include('apps.lms.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('reports/', include('apps.reports.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('cms/', include('apps.cms.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
