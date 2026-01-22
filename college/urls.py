from django.urls import path
from .views import (
    CollegeAPIRootView,
    CollegeTabsAPIView,
    CollegeCardsAPIView,
    CollegeHistoryAPIView,
    CollegeAboutAPIView,
    CollegeManagementAPIView,
    CollegeTeachersAPIView,
    CollegeSpecializationsAPIView,
    CollegeDepartmentsAPIView,
    CollegeMissionStrategyAPIView,
    DownloadResumeView,
    DownloadMissionStrategyPDFView,
    GalleryCardListAPIView
)

app_name = "college"

urlpatterns = [
    path("", CollegeAPIRootView.as_view(), name="api-root"),
    path("gallery-cards/", GalleryCardListAPIView.as_view(), name="gallery-cards"),
    path("tabs/", CollegeTabsAPIView.as_view(), name="tabs"),
    path("cards/", CollegeCardsAPIView.as_view(), name="cards"),
    path("history/", CollegeHistoryAPIView.as_view(), name="history"),
    path("about/", CollegeAboutAPIView.as_view(), name="about"),
    path(
        "management/", CollegeManagementAPIView.as_view(), name="management"
    ),
    path(
        "teachers/", CollegeTeachersAPIView.as_view(), name="teachers"
    ),
    path(
        "specializations/",
        CollegeSpecializationsAPIView.as_view(),
        name="specializations",
    ),
    path(
        "departments/",
        CollegeDepartmentsAPIView.as_view(),
        name="departments",
    ),
    path(
        "mission-strategy/",
        CollegeMissionStrategyAPIView.as_view(),
        name="mission-strategy",
    ),
    path(
        "resume/<str:model_type>/<int:pk>/",
        DownloadResumeView.as_view(),
        name="download-resume",
    ),
    path(
        "mission-strategy/pdf/<int:pk>/",
        DownloadMissionStrategyPDFView.as_view(),
        name="download-mission-strategy-pdf",
    ),
    path(
        "mission-strategy/pdf/<int:pk>/<str:lang>/",
        DownloadMissionStrategyPDFView.as_view(),
        name="download-mission-strategy-pdf-lang",
    ),
]