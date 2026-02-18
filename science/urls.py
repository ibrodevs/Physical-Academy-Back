from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_main import ScientificPublicationListView

# Import Publication views from views_main
from .views_main import (
    PublicationsViewSet,
    PublicationStatsViewSet,
    PublicationsPageView,
    VestnikYearViewSet,
)

# Import other views from views package
from .views import (
    # VestnikIssuesViewSet,
    # VestnikArticlesViewSet,
    # VestnikStatsViewSet,
    # VestnikPageView,
    ScopusMetricsViewSet,
    ScopusDocumentTypeViewSet,
    ScopusPublicationViewSet,
    ScopusAuthorViewSet,
    ScopusJournalViewSet,
    ScopusPublisherViewSet,
    ScopusPublicationAuthorViewSet,
    ScopusSectionViewSet,
    ScopusStatsViewSet,
    ScopusPageView,
    NTSCommitteeRoleViewSet,
    NTSResearchDirectionViewSet,
    NTSCommitteeMemberViewSet,
    NTSCommitteeSectionViewSet,
    NTSCommitteePageView,
    WebOfScienceTimeRangeViewSet,
    WebOfScienceMetricViewSet,
    WebOfScienceCategoryViewSet,
    WebOfScienceCollaborationViewSet,
    WebOfScienceJournalQuartileViewSet,
    WebOfScienceAdditionalMetricViewSet,
    WebOfScienceSectionViewSet,
    WebOfSciencePageView,
    StudentScientificSocietyInfoViewSet,
    StudentScientificSocietyStatViewSet,
    StudentScientificSocietyFeatureViewSet,
    StudentScientificSocietyProjectViewSet,
    StudentScientificSocietyEventViewSet,
    StudentScientificSocietyJoinStepViewSet,
    StudentScientificSocietyLeaderViewSet,
    StudentScientificSocietyContactViewSet,
    StudentScientificSocietyPageView,
)

# Create router and register viewsets
router = DefaultRouter()

router.register(r"publications", PublicationsViewSet)
router.register(r"publication-stats", PublicationStatsViewSet)


router.register(r"scopus-metrics", ScopusMetricsViewSet)
router.register(r"scopus-document-types", ScopusDocumentTypeViewSet)
router.register(r"scopus-publications", ScopusPublicationViewSet)
router.register(r"scopus-stats", ScopusStatsViewSet)
router.register(r"scopus-authors", ScopusAuthorViewSet)
router.register(r"scopus-journals", ScopusJournalViewSet)
router.register(r"scopus-publishers", ScopusPublisherViewSet)
router.register(r"scopus-publication-authors", ScopusPublicationAuthorViewSet)
router.register(r"scopus-sections", ScopusSectionViewSet)
# NTS Committee API endpoints
router.register(r"nts-committee-roles", NTSCommitteeRoleViewSet)
router.register(r"nts-research-directions", NTSResearchDirectionViewSet)
router.register(r"nts-committee-members", NTSCommitteeMemberViewSet)
router.register(r"nts-committee-sections", NTSCommitteeSectionViewSet)

# Web of Science API endpoints
router.register(r"wos-time-ranges", WebOfScienceTimeRangeViewSet)
router.register(r"wos-metrics", WebOfScienceMetricViewSet)
router.register(r"wos-categories", WebOfScienceCategoryViewSet)
router.register(r"wos-collaborations", WebOfScienceCollaborationViewSet)
router.register(r"wos-journal-quartiles", WebOfScienceJournalQuartileViewSet)
router.register(r"wos-additional-metrics", WebOfScienceAdditionalMetricViewSet)
router.register(r"wos-sections", WebOfScienceSectionViewSet)

# Student Scientific Society API endpoints
router.register(r"sss-info", StudentScientificSocietyInfoViewSet)
router.register(r"sss-stats", StudentScientificSocietyStatViewSet)
router.register(r"sss-features", StudentScientificSocietyFeatureViewSet)
router.register(r"sss-projects", StudentScientificSocietyProjectViewSet)
router.register(r"sss-events", StudentScientificSocietyEventViewSet)
router.register(r"sss-join-steps", StudentScientificSocietyJoinStepViewSet)
router.register(r"sss-leadership", StudentScientificSocietyLeaderViewSet)
router.register(r"sss-contacts", StudentScientificSocietyContactViewSet)

urlpatterns = [
    # ViewSet routes
    path("", include(router.urls)),
    # Additional views
    path(
        "publications-page/", PublicationsPageView.as_view(), name="publications-page"
    ),
    path("vestnik-page/", VestnikYearViewSet.as_view(), name="vestnik-page"),
    # Scopus page view
    path("scopus-page/", ScopusPageView.as_view(), name="scopus-page"),
    # NTS Committee page view
    path(
        "nts-committee-page/", NTSCommitteePageView.as_view(), name="nts-committee-page"
    ),
    # Web of Science page view
    path("wos-page/", WebOfSciencePageView.as_view(), name="wos-page"),
    # Student Scientific Society page view
    path(
        "student-scientific-society-page/",
        StudentScientificSocietyPageView.as_view(),
        name="student-scientific-society-page",
    ),

    path(
        "scientific-publications/",
        ScientificPublicationListView.as_view(),
        name="scientific-publications",
    ),

]
