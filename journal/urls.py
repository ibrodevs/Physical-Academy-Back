from django.urls import path
from .views import (
    JournalSectionView,
    EditorialBoardView,
    ArchiveListView,
    ArchiveByYearView,
    LatestIssueView,
)

urlpatterns = [
    path("editorial-board/",        EditorialBoardView.as_view(),  name="editorial-board"),
    path("archive/",                ArchiveListView.as_view(),     name="archive-list"),
    path("archive/<int:year>/",     ArchiveByYearView.as_view(),   name="archive-by-year"),
    path("latest-issue/",           LatestIssueView.as_view(),     name="latest-issue"),
    path("<str:section>/",          JournalSectionView.as_view(),  name="journal-section"),
]