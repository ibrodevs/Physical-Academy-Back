from django.urls import path
from .views import (
    JournalSectionView,
    EditorialOfficeView,
    EditorialBoardView,
    JournalArchiveView,
    LatestIssueView,
)

urlpatterns = [
    path("editorial-office/", EditorialOfficeView.as_view(), name="editorial-office"),
    path("editorial-board/",  EditorialBoardView.as_view(),  name="editorial-board"),
    path("archive/",          JournalArchiveView.as_view(),  name="journal-archive"),
    path("latest-issue/",     LatestIssueView.as_view(),     name="latest-issue"),
    path("<str:section>/",    JournalSectionView.as_view(),  name="journal-section"),  # последним!
]
