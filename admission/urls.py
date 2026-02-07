from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CollegeAdmissionRequirementsViewSet, CollegeAdmissionStepsViewSet, CollegeProgramsViewSet, CollegeSoonEventsViewSet, CollegeStatisticsViewSet,  QuotaTypeViewSet, QuotaStatsViewSet, AdditionalSupportViewSet,
    ProcessStepViewSet, BachelorQuotasViewSet, 
    MasterListAPIView,
    AspirantDocumentsViewSet, AspirantProgramsViewSet, AspirantMainDateViewSet, AspirantRequirementsViewSet, 
    BachelorProgramViewSet, DoctorateListAPIView
)

# Создаем роутер для API
router = DefaultRouter()
router.register(r'quota-types', QuotaTypeViewSet, basename='quota-types')
router.register(r'quota-stats', QuotaStatsViewSet, basename='quota-stats')
router.register(r'additional-support', AdditionalSupportViewSet, basename='additional-support')
router.register(r'process-steps', ProcessStepViewSet, basename='process-steps')
router.register(r'bachelor-quotas', BachelorQuotasViewSet, basename='bachelor-quotas')
router.register(r'bachelor-programs', BachelorProgramViewSet, basename='bachelor-programs')

router.register(r'aspirant-documents', AspirantDocumentsViewSet, basename='aspirant-documents')
router.register(r'aspirant-programs', AspirantProgramsViewSet, basename='aspirant-programs')
router.register(r'aspirant-main-dates', AspirantMainDateViewSet, basename='aspirant-main-dates')
router.register(r'aspirant-requirements', AspirantRequirementsViewSet, basename='aspirant-requirements')
router.register(r'college-soon-events', CollegeSoonEventsViewSet, basename='college-soon-events')
router.register(r'college-admission-steps', CollegeAdmissionStepsViewSet, basename='college-admission-steps')
router.register(r'college-admission-requirements', CollegeAdmissionRequirementsViewSet, basename='college-admission-requirements')
router.register(r'college-statistics', CollegeStatisticsViewSet, basename='college-statistics')

college_programs_list = CollegeProgramsViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('', include(router.urls)),
    path('master/', MasterListAPIView.as_view(), name='master'),
    path('doctorate/', DoctorateListAPIView.as_view(), name='doctorate'),
    path('college-programs/', college_programs_list, name='college-programs'),
]