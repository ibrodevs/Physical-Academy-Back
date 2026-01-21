from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import (
    BoardOfTrustees,
    AuditCommission,
    AcademicCouncil,
    Profsoyuz,
    AdministrativeDepartment,
    AdministrativeUnit,
    Leadership,
    OrganizationStructure,
    Document,
)
from .serializers import (
    BoardOfTrusteesSerializer,
    AuditCommissionSerializer,
    AcademicCouncilSerializer,
    ProfsoyuzSerializer,
    AdministrativeDepartmentSerializer,
    AdministrativeUnitSerializer,
    LeadershipSerializer,
    OrganizationStructureSerializer,
    LeadershipSerializer,
    DocumentSerializer,
)



class BoardOfTrusteesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BoardOfTrustees.objects.all()

    serializer_class = BoardOfTrusteesSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

   
class AuditCommissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditCommission.objects.all()
    serializer_class = AuditCommissionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

class ProfsoyuzViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profsoyuz.objects.all()
    serializer_class = ProfsoyuzSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context


class AuditCommissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Audit Commission members.
    Provides read-only access with multilingual support.
    """

    serializer_class = AuditCommissionSerializer

    def get_queryset(self):
        # Check for swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            return AuditCommission.objects.none()
        return AuditCommission.objects.filter(is_active=True)


class AcademicCouncilViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Academic Council members.
    Provides read-only access with multilingual support.
    """

    serializer_class = AcademicCouncilSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "name_kg", "name_en", "position", "department"]
    ordering_fields = ["order", "name", "created_at"]
    ordering = ["order", "name"]

    def get_queryset(self):
        # Check for swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            return AcademicCouncil.objects.none()
        return AcademicCouncil.objects.filter(is_active=True)


@extend_schema_view(
    list=extend_schema(
        summary="Get list of Trade Union benefits",
        description="Retrieve all active Trade Union benefits with multilingual support (ru, kg, en).",
        tags=["Leadership Structure - Trade Union"],
        parameters=[
            OpenApiParameter(
                name="lang",
                description="Language code (ru, kg, en)",
                required=False,
                type=str,
            ),
        ],
    ),
)




class AdministrativeDepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Administrative Departments.
    Provides read-only access with multilingual support.
    """

    serializer_class = AdministrativeDepartmentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "name_kg", "name_en", "head"]
    ordering_fields = ["order", "name", "created_at"]
    ordering = ["order", "name"]

    def get_queryset(self):
        # Check for swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            return AdministrativeDepartment.objects.none()
        return AdministrativeDepartment.objects.filter(is_active=True)


@extend_schema_view(
    list=extend_schema(
        summary="Get list of Administrative Units",
        description="Retrieve all active administrative units with multilingual support (ru, kg, en).",
        tags=["Leadership Structure - Administrative"],
        parameters=[
            OpenApiParameter(
                name="lang",
                description="Language code (ru, kg, en)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="search",
                description="Search by name, description, or head",
                required=False,
                type=str,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Get Administrative Unit details",
        description="Retrieve detailed information about a specific unit.",
        tags=["Leadership Structure - Administrative"],
    ),
)
class AdministrativeUnitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Administrative Units.
    Provides read-only access with multilingual support and search functionality.
    """

    serializer_class = AdministrativeUnitSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "name_kg", "name_en", "description", "head"]
    ordering_fields = ["order", "name", "created_at"]
    ordering = ["order", "name"]

    def get_queryset(self):
        # Check for swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            return AdministrativeUnit.objects.none()
        return AdministrativeUnit.objects.filter(is_active=True)


# ========== NEW VIEWSETS FOR MISSING APIs ==========


class LeadershipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leadership.objects.all().order_by('order')
    serializer_class = LeadershipSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context


@extend_schema_view(
    list=extend_schema(
        summary="Get Organization Structure",
        description="Retrieve hierarchical organization structure with multilingual support.",
        tags=["Leadership Structure - Organization"],
        parameters=[
            OpenApiParameter(
                name="lang",
                description="Language code (ru, kg, en)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="structure_type",
                description="Filter by structure type",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="parent",
                description="Filter by parent ID (null for root elements)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="search",
                description="Search by name or head",
                required=False,
                type=str,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Get Organization Structure details",
        description="Retrieve detailed information about a specific structure unit.",
        tags=["Leadership Structure - Organization"],
    ),
)
class OrganizationStructureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Organization Structure.
    Provides hierarchical structure with multilingual support.
    """

    serializer_class = OrganizationStructureSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["structure_type", "parent"]
    search_fields = ["name", "name_kg", "name_en", "head"]
    ordering_fields = ["order", "name", "created_at"]
    ordering = ["order", "name"]

    def get_queryset(self):
        # Check for swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            return OrganizationStructure.objects.none()
        return OrganizationStructure.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

    @action(detail=False, methods=["get"])
    def root(self, request):
        """Get root level structure units (without parent)"""
        root_structures = self.get_queryset().filter(parent__isnull=True)
        serializer = self.get_serializer(root_structures, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Get list of Documents",
        description="Retrieve all active documents with multilingual support and filtering.",
        tags=["Leadership Structure - Documents"],
        parameters=[
            OpenApiParameter(
                name="lang",
                description="Language code (ru, kg, en)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="document_type",
                description="Filter by document type",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="is_featured",
                description="Filter featured documents",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="search",
                description="Search by title or description",
                required=False,
                type=str,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Get Document details",
        description="Retrieve detailed information about a specific document.",
        tags=["Leadership Structure - Documents"],
    ),
)
class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Documents.
    Provides read-only access with multilingual support and filtering.
    """

    serializer_class = DocumentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["document_type", "is_featured"]
    search_fields = ["title", "title_kg", "title_en", "description", "document_number"]
    ordering_fields = ["order", "title", "document_date", "created_at"]
    ordering = ["-document_date", "order", "title"]

    def get_queryset(self):
        # Check for swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            return Document.objects.none()
        return Document.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

    @action(detail=False, methods=["get"])
    def featured(self, request):
        """Get featured documents"""
        featured_docs = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_docs, many=True)
        return Response(serializer.data)
