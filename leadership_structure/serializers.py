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
)




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

    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Profsoyuz
        fields = [
            "id",
            "title",

            "description",

            "image_url",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj) -> str:
        return self.get_translated_field(obj, "title")

    def get_description(self, obj) -> str:
        return self.get_translated_field(obj, "description")
    
    def get_image_url(self, obj) -> str:
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None



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

class AcademicCouncilSerializer(
    MultiLanguageSerializerMixin, serializers.ModelSerializer
):
    """Serializer for Academic Council"""

    name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AcademicCouncil
        fields = [
            "id",
            "name",
            "name_kg",
            "name_en",
            "position",
            "position_kg",
            "position_en",
            "department",
            "department_kg",
            "department_en",
            "achievements",
            "achievements_kg",
            "achievements_en",
            "email",
            "phone",
            "image",
            "image_url",
            "order",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        return self.get_translated_field(obj, "name")

    @extend_schema_field(OpenApiTypes.STR)
    def get_position(self, obj) -> str:
        return self.get_translated_field(obj, "position")

    @extend_schema_field(OpenApiTypes.STR)
    def get_department(self, obj) -> str:
        return self.get_translated_field(obj, "department")

    @extend_schema_field(OpenApiTypes.STR)
    def get_achievements(self, obj) -> str:
        return self.get_translated_json_field(obj, "achievements")

    @extend_schema_field(OpenApiTypes.STR)
    def get_image_url(self, obj) -> str:
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None




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


class AdministrativeUnitSerializer(
    MultiLanguageSerializerMixin, serializers.ModelSerializer
):
    """Serializer for Administrative Units"""

    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    head = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    staff = serializers.SerializerMethodField()
    responsibilities = serializers.SerializerMethodField()

    class Meta:
        model = AdministrativeUnit
        fields = [
            "id",
            "name",
            "name_kg",
            "name_en",
            "description",
            "description_kg",
            "description_en",
            "head",
            "head_kg",
            "head_en",
            "location",
            "location_kg",
            "location_en",
            "staff",
            "staff_kg",
            "staff_en",
            "responsibilities",
            "responsibilities_kg",
            "responsibilities_en",
            "email",
            "phone",
            "icon",
            "color",
            "color_class",
            "order",
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
    def get_location(self, obj) -> str:
        return self.get_translated_field(obj, "location")

    @extend_schema_field(OpenApiTypes.STR)
    def get_staff(self, obj) -> str:
        return self.get_translated_field(obj, "staff")

    @extend_schema_field(OpenApiTypes.STR)
    def get_responsibilities(self, obj) -> str:
        return self.get_translated_json_field(obj, "responsibilities")


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

    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    file_size_formatted = serializers.SerializerMethodField()
    document_type_display = serializers.SerializerMethodField()

    # Document type translations
    DOCUMENT_TYPE_TRANSLATIONS = {
        "regulation": {"ru": "Положение", "en": "Regulation", "kg": "Жобо"},
        "order": {"ru": "Приказ", "en": "Order", "kg": "Буйрук"},
        "instruction": {"ru": "Инструкция", "en": "Instruction", "kg": "Нускама"},
        "charter": {"ru": "Устав", "en": "Charter", "kg": "Устав"},
        "plan": {"ru": "План", "en": "Plan", "kg": "План"},
        "report": {"ru": "Отчет", "en": "Report", "kg": "Отчет"},
        "other": {"ru": "Другое", "en": "Other", "kg": "Башка"},
    }

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "document_type",
            "document_type_display",
            "description",
            "file",
            "file_url",
            "document_number",
            "document_date",
            "file_size",
            "file_size_formatted",
            "file_format",
            "icon",
            "is_active",
            "is_featured",
            "order",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj) -> str:
        return self.get_translated_field(obj, "title")

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj) -> str:
        return self.get_translated_field(obj, "description")

    @extend_schema_field(OpenApiTypes.STR)
    def get_file_url(self, obj) -> str:
        """Get absolute URL for file"""
        if obj.file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

    @extend_schema_field(OpenApiTypes.STR)
    def get_file_size_formatted(self, obj) -> str:
        """Format file size in human readable format"""
        if obj.file_size:
            if obj.file_size < 1024:
                return f"{obj.file_size} B"
            elif obj.file_size < 1024 * 1024:
                return f"{obj.file_size / 1024:.1f} KB"
            else:
                return f"{obj.file_size / (1024 * 1024):.1f} MB"
        return "N/A"

    @extend_schema_field(OpenApiTypes.STR)
    def get_document_type_display(self, obj) -> str:
        """Get localized document type display name"""
        lang = self.context.get("language", "ru")
        document_type = obj.document_type

        # Get translation from DOCUMENT_TYPE_TRANSLATIONS
        translations = self.DOCUMENT_TYPE_TRANSLATIONS.get(document_type, {})
        return translations.get(lang, translations.get("ru", document_type))
