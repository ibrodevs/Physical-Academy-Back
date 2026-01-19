from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutStatisticsViewSet, AboutPhotosViewSet, AcademyInfrastructureViewSet, MissionViewSet, AccreditationViewSet, AcademyAchievementsViewSet, AcademyStatisticsViewSet, HistoryViewSet

router = DefaultRouter()
router.register(r'about-statistics', AboutStatisticsViewSet)
router.register(r'about-photos', AboutPhotosViewSet)
router.register(r'missions', MissionViewSet)
router.register(r'accreditations', AccreditationViewSet)
router.register(r'achievements', AcademyAchievementsViewSet)
router.register(r'statistics', AcademyStatisticsViewSet)
router.register(r'infrastructure', AcademyInfrastructureViewSet)
router.register(r'history', HistoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
