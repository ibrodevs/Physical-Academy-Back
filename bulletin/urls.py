from django.urls import path
from .views import BulletinSidebarView, BulletinIssueDetailView

urlpatterns = [
    # GET /api/bulletin/sidebar/?lang=ru
    path('sidebar/', BulletinSidebarView.as_view(), name='bulletin-sidebar'),

    # GET /api/bulletin/issues/1/?lang=ru
    path('issues/<int:pk>/', BulletinIssueDetailView.as_view(), name='bulletin-issue-detail'),
]