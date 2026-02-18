# This file is deprecated and kept only for backward compatibility
# All views are now split between views_main.py and views/ package
from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import ScientificPublication
from .serializers_main import ScientificPublicationSerializer

from .models import (
    Publication,
    PublicationStats,
    VestnikYear,
    VestnikRelease
)
from .serializers_main import (
    PublicationSerializer,
    PublicationStatsSerializer,
    PublicationsPageSerializer,
    VestnikYearSerializer,
    VestnikReleaseSerializer,
)


# Other views are imported from views/ package (will be migrated later)
from .views import (
    NTSCommitteeRoleViewSet,
    NTSResearchDirectionViewSet,
    NTSCommitteeMemberViewSet,
    NTSCommitteePageView,
    ScopusMetricsViewSet,
    ScopusDocumentTypeViewSet,
    ScopusPublicationViewSet,
    ScopusStatsViewSet,
    ScopusPageView,
    WebOfScienceTimeRangeViewSet,
    WebOfScienceMetricViewSet,
    WebOfScienceCategoryViewSet,
    WebOfScienceCollaborationViewSet,
    WebOfScienceJournalQuartileViewSet,
    WebOfScienceAdditionalMetricViewSet,
    WebOfScienceSectionViewSet,
    WebOfSciencePageView,
)

__all__ = [
    "PublicationsViewSet",
    "PublicationStatsViewSet",
    "PublicationsPageView",
    "VestnikYearsViewSet",
    "VestnikReleasesViewSet",
    "NTSCommitteeRoleViewSet",
    "NTSResearchDirectionViewSet",
    "NTSCommitteeMemberViewSet",
    "NTSCommitteePageView",
    "ScopusMetricsViewSet",
    "ScopusDocumentTypeViewSet",
    "ScopusPublicationViewSet",
    "ScopusStatsViewSet",
    "ScopusPageView",
    "WebOfScienceTimeRangeViewSet",
    "WebOfScienceMetricViewSet",
    "WebOfScienceCategoryViewSet",
    "WebOfScienceCollaborationViewSet",
    "WebOfScienceJournalQuartileViewSet",
    "WebOfScienceAdditionalMetricViewSet",
    "WebOfScienceSectionViewSet",
    "WebOfSciencePageView",
    "ScientificPublicationListView",

]


# ==================== PUBLICATION VIEWS ====================


class PublicationsViewSet(viewsets.ModelViewSet):
    """ViewSet for managing publications"""

    queryset = Publication.objects.all().order_by("order", "-year", "-id")
    serializer_class = PublicationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by type if specified
        pub_type = self.request.query_params.get("type")
        if pub_type:
            queryset = queryset.filter(publication_type=pub_type)

        # Filter by search term if provided
        search = self.request.query_params.get("search")
        if search:
            # Search across all language versions
            queryset = queryset.filter(
                Q(title_ru__icontains=search)
                | Q(title_en__icontains=search)
                | Q(title_kg__icontains=search)
                | Q(author_ru__icontains=search)
                | Q(author_en__icontains=search)
                | Q(author_kg__icontains=search)
            )

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context


class PublicationStatsViewSet(viewsets.ModelViewSet):
    """ViewSet for managing publication statistics"""

    queryset = PublicationStats.objects.all().order_by("order")
    serializer_class = PublicationStatsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context


class PublicationsPageView(generics.GenericAPIView):
    """View for the complete publications page data"""

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="lang",
                description="Language code (ru, en, kg)",
                required=False,
                type=str,
                default="ru",
            ),
            OpenApiParameter(
                name="type",
                description="Filter by publication type",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="search",
                description="Search term for filtering publications",
                required=False,
                type=str,
            ),
        ]
    )
    def get(self, request):
        # Get stats
        stats = PublicationStats.objects.all().order_by("order")

        # Get featured publications
        featured = Publication.objects.filter(is_featured=True).order_by(
            "order", "-year", "-id"
        )

        # Get regular publications with filters
        publications = Publication.objects.filter(is_featured=False).order_by(
            "order", "-year", "-id"
        )

        # Apply type filter if specified
        pub_type = request.query_params.get("type")
        if pub_type:
            publications = publications.filter(publication_type=pub_type)

        # Apply search filter if specified
        search = request.query_params.get("search")
        if search:
            publications = publications.filter(
                Q(title_ru__icontains=search)
                | Q(title_en__icontains=search)
                | Q(title_kg__icontains=search)
                | Q(author_ru__icontains=search)
                | Q(author_en__icontains=search)
                | Q(author_kg__icontains=search)
            )

        # Prepare context with language
        context = {
            "request": request,
            "language": request.query_params.get("lang", "ru"),
        }

        # Serialize all components
        serializer = PublicationsPageSerializer(
            {"stats": stats, "featured": featured, "publications": publications},
            context=context,
        )

        return Response(serializer.data)


# ==================== VESTNIK VIEWS ====================


class VestnikYearViewSet(generics.ListAPIView):
    """ViewSet for listing Vestnik years with their releases"""

    queryset = VestnikYear.objects.all().prefetch_related("releases")
    serializer_class = VestnikYearSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

# ==================== SCIENTIFIC PUBLICATION VIEWS ====================


class ScientificPublicationListView(generics.ListAPIView):
    """Public API for Scientific Publications (PDF section)"""

    queryset = ScientificPublication.objects.all().order_by("-created_at")
    serializer_class = ScientificPublicationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context



