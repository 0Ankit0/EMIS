"""
EMIS URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/v1/', include('apps.core.api_urls')),
    
    # Frontend URLs
    path('', include('apps.core.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('student/', include('apps.students.urls')),
    path('faculty/', include('apps.faculty.urls')),
    path('admin-portal/', include('apps.hr.urls')),
    path('finance/', include('apps.finance.urls')),
    path('library/', include('apps.library.urls')),
    path('lms/', include('apps.lms.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
