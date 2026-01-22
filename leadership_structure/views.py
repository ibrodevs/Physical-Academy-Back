from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import (
    BoardOfTrustees,
    AuditCommission,
    AcademicCouncil,
    Commission,
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
    CommissionSerializer,
    ProfsoyuzSerializer,
    AdministrativeDepartmentSerializer,
    AdministrativeUnitSerializer,
    LeadershipSerializer,
    OrganizationStructureSerializer,
    LeadershipSerializer,
    DocumentSerializer,
)


class CommissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

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

class AcademicCouncilViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AcademicCouncil.objects.all()
    serializer_class = AcademicCouncilSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context



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


class AdministrativeUnitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Administrative Units.
    Provides read-only access with multilingual support and search functionality.
    """
    queryset = AdministrativeUnit.objects.all()
    serializer_class = AdministrativeUnitSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

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


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Documents.
    Provides read-only access with multilingual support and filtering.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
   
 
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context
