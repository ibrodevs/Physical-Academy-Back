from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BoardOfTrusteesViewSet,
    AuditCommissionViewSet,
    ProfsoyuzViewSet,
    AcademicCouncilViewSet,
    AdministrativeDepartmentViewSet, AdministrativeUnitViewSet,
    LeadershipViewSet, OrganizationStructureViewSet, DocumentViewSet, CommissionViewSet
)

router = DefaultRouter()

router.register(r'commissions', CommissionViewSet, basename='commissions')

# Board of Trustees
router.register(r'board-of-trustees', BoardOfTrusteesViewSet, basename='board-of-trustees')

# Audit Commission
router.register(r'audit-commission', AuditCommissionViewSet, basename='audit-commission')

# Academic Council
router.register(r'academic-council', AcademicCouncilViewSet, basename='academic-council')



# Trade Union
router.register(r'profsoyuz', ProfsoyuzViewSet, basename='profsoyuz')

# Commissions

# Administrative Structure
router.register(r'administrative/departments', AdministrativeDepartmentViewSet, basename='administrative-departments')
router.register(r'administrative/units', AdministrativeUnitViewSet, basename='administrative-units')

# New APIs for missing endpoints
router.register(r'leadership', LeadershipViewSet, basename='leadership')
router.register(r'organization-structure', OrganizationStructureViewSet, basename='organization-structure')
router.register(r'documents', DocumentViewSet, basename='documents')

urlpatterns = [
    path('', include(router.urls)),
]
