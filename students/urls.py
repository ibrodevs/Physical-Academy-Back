from django.urls import path
from .views import (
    StudentSupportListAPIView,
    StudentsCounseilListAPIView,
    StudentExchangeListAPIView,
    StudentInstractionsListAPIView,
    ScholarshipProgramListAPIView,
    ScholarshipRequiredDocumentListAPIView,
)

urlpatterns = [
    path('support/', StudentSupportListAPIView.as_view(), name='student-support'),
    path('council/', StudentsCounseilListAPIView.as_view(), name='students-council'),
    path('exchange/', StudentExchangeListAPIView.as_view(), name='student-exchange'),
    path('instructions/', StudentInstractionsListAPIView.as_view(), name='student-instructions'),
    path('scholarships/', ScholarshipProgramListAPIView.as_view(), name='scholarship-programs'),
    path('scholarships/documents/', ScholarshipRequiredDocumentListAPIView.as_view(), name='scholarship-documents'),
]
