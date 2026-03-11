from django.urls import path
from .views import (
    JournalSectionView,
    EditorialBoardView,
    ArchiveListView,
    ArchiveByYearView,
    LatestIssueView,
    EditorialOfficeListView,
    EditorialOfficeDetailView,
    ThemeRegistryListView,
    RegulationListView
)

urlpatterns = [
    path("editorial-office/",          EditorialOfficeListView.as_view(),   name="editorial-office-list"),
    path("editorial-office/<int:pk>/", EditorialOfficeDetailView.as_view(), name="editorial-office-detail"),
    path("editorial-board/",        EditorialBoardView.as_view(),  name="editorial-board"),
    path("archive/",                ArchiveListView.as_view(),     name="archive-list"),
    path("archive/<int:year>/",     ArchiveByYearView.as_view(),   name="archive-by-year"),
    path("latest-issue/",           LatestIssueView.as_view(),     name="latest-issue"),
    path("theme-registry/", ThemeRegistryListView.as_view(), name="theme-registry"),
    path("regulations/",    RegulationListView.as_view(),    name="regulations"),
    path("<str:section>/",          JournalSectionView.as_view(),  name="journal-section"),
]