from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SportAchievementViewSet

router = DefaultRouter()
router.register(r"sport-achievements", SportAchievementViewSet, basename="sport-achievement")

urlpatterns = [
    path("", include(router.urls)),
]
