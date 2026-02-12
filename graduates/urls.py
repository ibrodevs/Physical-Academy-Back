from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GraduateViewSet

router = DefaultRouter()
router.register(r"graduates", GraduateViewSet, basename="graduate")

urlpatterns = [
    path("", include(router.urls)),
]
