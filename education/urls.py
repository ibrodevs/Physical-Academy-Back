from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MasterListAPIView,
    PhdListAPIView,
    CollegeDepartmentCategoriesAPIView,
    CollegeDepartmentCategoryDetailAPIView,
    CollegeFacultyManagementAPIView,
)

urlpatterns = [
    path("master/", MasterListAPIView.as_view(), name='master'), 
    path("phd/", PhdListAPIView.as_view(), name='Phd'), 
    path("college-categories/", CollegeDepartmentCategoriesAPIView.as_view(), name="college-categories"),
    path(
        "college-categories/<int:id>/",
        CollegeDepartmentCategoryDetailAPIView.as_view(),
        name="college-category-detail",
    ),
    path("college-management/", CollegeFacultyManagementAPIView.as_view(), name="college-management"),
]
