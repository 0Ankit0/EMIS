from django.urls import path
from .views import ExamAutomationView

urlpatterns = [
    path('process/', ExamAutomationView.as_view(), name='process-exam'),
]
