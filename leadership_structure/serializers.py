from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
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
    Commission,

)


class CommissionSerializer(serializers.ModelSerializer):
    """Serializer for Commission"""

    text = serializers.SerializerMethodField()

    class Meta:
        model = Commission
        fields = [
           'id', "text",
        ]

    def get_text(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_text(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        return obj.get_name(self.context.get("language", "ru"))

    @extend_schema_field(OpenApiTypes.STR)
    def get_position(self, obj) -> str:
        return obj.get_position(self.context.get("language", "ru"))

    @extend_schema_field(OpenApiTypes.STR)
    def get_image_url(self, obj) -> str:
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None

class MultiLanguageSerializerMixin:
    """Mixin for handling multi-language fields"""

    def get_language(self):
        """Get language from request context"""
        request = self.context.get("request")
        if request:
            # Only use explicit lang parameter, default to Russian
            language = request.GET.get("lang", "ru")
            # Normalize legacy code 'ky' to 'kg' for backward compatibility
            if language == "ky":
                language = "kg"
            return language
        return "ru"

    def get_translated_field(self, obj, field_name):
        """Get field value in the requested language"""
        language = self.get_language()

        if language == "kg":
            translated_value = getattr(obj, f"{field_name}_kg", None)
            if (
                translated_value and translated_value.strip()
            ):  # Check for non-empty string
                return translated_value
        elif language == "en":
            translated_value = getattr(obj, f"{field_name}_en", None)
            if (
                translated_value and translated_value.strip()
            ):  # Check for non-empty string
                return translated_value

        # Fallback to Russian
        return getattr(obj, field_name)

    def get_translated_json_field(self, obj, field_name):
        """Get JSON field value in the requested language"""
        language = self.get_language()

        if language == "kg":
            translated_value = getattr(obj, f"{field_name}_kg", None)
            if translated_value and len(translated_value) > 0:
                return translated_value
        elif language == "en":
            translated_value = getattr(obj, f"{field_name}_en", None)
            if translated_value and len(translated_value) > 0:
                return translated_value

        # Fallback to Russian
        return getattr(obj, field_name, [])

class AuditCommissionSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = AuditCommission
        fields = [
            "id",
            "text",
        ]
        
    def get_text(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_text(language)
    
class ProfsoyuzSerializer(serializers.ModelSerializer):
    """Serializer for Profsoyuz"""

    description = serializers.SerializerMethodField()

    class Meta:
        model = Profsoyuz
        fields = [
            "id",

            "description",

        ]

    def get_description(self, obj) -> str:
        return obj.get_description(self.context.get("language", "ru"))
    




class BoardOfTrusteesSerializer(
    MultiLanguageSerializerMixin, serializers.ModelSerializer
):
    """Serializer for Board of Trustees"""

    name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
  

    class Meta:
        model = BoardOfTrustees
        fields = [
            "name",

            "position",
            "image",
            "image_url",

        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        return self.get_translated_field(obj, "name")

    @extend_schema_field(OpenApiTypes.STR)
    def get_position(self, obj) -> str:
        return self.get_translated_field(obj, "position")

    @extend_schema_field(OpenApiTypes.STR)
    def get_image_url(self, obj) -> str:
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
\

class AcademicCouncilSerializer(serializers.ModelSerializer):
    """Serializer for Academic Council"""

    text = serializers.SerializerMethodField()

    class Meta:
        model = AcademicCouncil
        fields= ['id','text']

    def get_text(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_text(language)




class AdministrativeDepartmentSerializer(
    MultiLanguageSerializerMixin, serializers.ModelSerializer
):
    """Serializer for Administrative Departments"""

    name = serializers.SerializerMethodField()
    head = serializers.SerializerMethodField()
    responsibilities = serializers.SerializerMethodField()

    class Meta:
        model = AdministrativeDepartment
        fields = [
            "id",
            "name",
            "name_kg",
            "name_en",
            "head",
            "head_kg",
            "head_en",
            "responsibilities",
            "responsibilities_kg",
            "responsibilities_en",
            "email",
            "phone",
            "icon",
            "order",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        return self.get_translated_field(obj, "name")

    @extend_schema_field(OpenApiTypes.STR)
    def get_head(self, obj) -> str:
        return self.get_translated_field(obj, "head")

    @extend_schema_field(OpenApiTypes.STR)
    def get_responsibilities(self, obj) -> str:
        return self.get_translated_json_field(obj, "responsibilities")


class AdministrativeUnitSerializer(serializers.ModelSerializer
):
    """Serializer for Administrative Units"""
    text = serializers.SerializerMethodField()

    class Meta:
        model = AdministrativeUnit
        fields = [
            "id",
            'text'
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_text(self, obj) -> str:
        return obj.get_text(self.context.get("language", "ru"))

# ========== NEW SERIALIZERS FOR MISSING APIs ==========


class LeadershipSerializer( serializers.ModelSerializer):
    """Сериалайзер для Leadership (для /leadership/)"""

    name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Leadership
        fields = [
            "id",
            'photo',
            'order',
            "name",
            "bio",
            'image_url',
            "position",
        ]

    def get_name(self, obj) -> str:
        return obj.get_name(self.context.get("language", "ru"))
    
    def get_position(self, obj):
        return obj.get_position(self.context.get("language", "ru"))
    
    def get_bio(self, obj):
        return obj.get_bio(self.context.get("language", "ru"))
    
    def get_image_url(self, obj) -> str:
        if obj.photo:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.photo.url)
        return None

class OrganizationStructureSerializer(
    MultiLanguageSerializerMixin, serializers.ModelSerializer
):
    """Сериалайзер для OrganizationStructure (для /organization-structure/)"""

    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    head = serializers.SerializerMethodField()
    responsibilities = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    structure_type_display = serializers.SerializerMethodField()

    # Structure type translations
    STRUCTURE_TYPE_TRANSLATIONS = {
        "faculty": {"ru": "Факультет", "en": "Faculty", "kg": "Факультети"},
        "department": {"ru": "Кафедра", "en": "Department", "kg": "Кафедрасы"},
        "unit": {"ru": "Подразделение", "en": "Unit", "kg": "Бөлүм"},
        "service": {"ru": "Служба", "en": "Service", "kg": "Кызмат"},
        "center": {"ru": "Центр", "en": "Center", "kg": "Борбор"},
    }

    class Meta:
        model = OrganizationStructure
        fields = [
            "id",
            "name",
            "structure_type",
            "structure_type_display",
            "description",
            "head",
            "parent",
            "responsibilities",
            "email",
            "phone",
            "location",
            "staff_count",
            "icon",
            "is_active",
            "order",
            "children",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        return self.get_translated_field(obj, "name")

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj) -> str:
        return self.get_translated_field(obj, "description")

    @extend_schema_field(OpenApiTypes.STR)
    def get_head(self, obj) -> str:
        return self.get_translated_field(obj, "head")

    @extend_schema_field(OpenApiTypes.STR)
    def get_responsibilities(self, obj) -> str:
        return self.get_translated_json_field(obj, "responsibilities")

    @extend_schema_field(OpenApiTypes.STR)
    def get_location(self, obj) -> str:
        return self.get_translated_field(obj, "location")

    # Для списка организаций возвращаем тип через inline-сериализатор
    # Удаляем аннотацию типа для метода, возвращающего список объектов
    # drf-spectacular автоматически определит правильный тип из сериализатора
    def get_children(self, obj) -> list:
        """Get child structures"""
        children = OrganizationStructure.objects.filter(
            parent=obj, is_active=True
        ).order_by("order", "name")
        return OrganizationStructureSerializer(
            children, many=True, context=self.context
        ).data

    @extend_schema_field(OpenApiTypes.STR)
    def get_structure_type_display(self, obj) -> str:
        """Get localized structure type display name"""
        lang = self.context.get("language", "ru")
        structure_type = obj.structure_type

        # Get translation from STRUCTURE_TYPE_TRANSLATIONS
        translations = self.STRUCTURE_TYPE_TRANSLATIONS.get(structure_type, {})
        return translations.get(lang, translations.get("ru", structure_type))


class DocumentSerializer(MultiLanguageSerializerMixin, serializers.ModelSerializer):
    """Сериалайзер для Document (для /documents/)"""

    name = serializers.SerializerMethodField()
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id",
            "name",
            "pdf",
        ]

    def get_name(self, obj):
        return obj.get_name(self.context.get("language", "ru"))
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_pdf(self, obj) -> str | None:
        language = self.context.get("language", "ru")
        pdf = getattr(obj, f"pdf_{language}", None)
        if not pdf:
            return None
        try:
            return pdf.url
        except Exception:
            return str(pdf)
        