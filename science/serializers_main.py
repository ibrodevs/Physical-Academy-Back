from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from .models import (
    Publication,
    PublicationStats,
    VestnikYear,
    VestnikRelease,
)



from .serializers.nts_committee import (
    NTSCommitteeRoleSerializer,
    NTSResearchDirectionSerializer,
    NTSCommitteeMemberSerializer,
    NTSCommitteeSectionSerializer,
)
from .serializers.scopus import (
    ScopusAuthorSerializer,
    ScopusJournalSerializer,
    ScopusPublisherSerializer,
    ScopusPublicationAuthorSerializer,
    ScopusPublicationSerializer,
)


from .models import ScientificPublication

# ==================== PUBLICATION SERIALIZERS ====================


class VestnikReleaseSerializer(serializers.ModelSerializer):
    """Сериализатор для выпусков Вестника с поддержкой многоязычности"""

    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = VestnikRelease
        fields = [
            "id",
            "title",
            "description",
            "pdf",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        language = self.context.get("language", "ru")
        return obj.get_title(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        language = self.context.get("language", "ru")
        return obj.get_description(language)

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
        

class VestnikYearSerializer(serializers.ModelSerializer):
    """Сериализатор для годов Вестника с вложенными выпусками"""

    releases = VestnikReleaseSerializer(many=True, read_only=True)

    class Meta:
        model = VestnikYear
        fields = ["id", "year", "releases"]




class PublicationSerializer(serializers.ModelSerializer):
    """Сериализатор для научных публикаций с поддержкой многоязычности"""

    title = serializers.SerializerMethodField()
    abstract = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()
    pub_type_display = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = [
            "id",
            "title",
            "authors",
            "abstract",
            "journal",
            "year",
            "doi",
            "url",
            "citation_count",
            "publication_type",
            "pub_type_display",
            "pdf_url",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        language = self.context.get("language", "ru")
        return obj.get_title(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_abstract(self, obj):
        language = self.context.get("language", "ru")
        return obj.get_abstract(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_authors(self, obj):
        language = self.context.get("language", "ru")
        return obj.get_authors(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_pub_type_display(self, obj):
        """Возвращает читаемое название типа публикации на выбранном языке"""
        type_mapping = {
            "article": {
                "ru": "Журнальная статья",
                "en": "Journal Article",
                "kg": "Журнал макаласы",
            },
            "conference": {
                "ru": "Конференция",
                "en": "Conference Paper",
                "kg": "Конференция",
            },
            "book": {"ru": "Книга/Глава", "en": "Book/Chapter", "kg": "Китеп/Бөлүм"},
            "patent": {"ru": "Патент", "en": "Patent", "kg": "Патент"},
        }
        language = self.context.get("language", "ru")
        return type_mapping.get(obj.publication_type, {}).get(
            language, obj.publication_type
        )

    @extend_schema_field(OpenApiTypes.STR)
    def get_pdf_url(self, obj):
        """Возвращает полный URL для PDF файла"""
        if obj.pdf_file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.pdf_file.url)
        return None


# ==================== PUBLICATION STATS SERIALIZERS ====================


class PublicationStatsSerializer(serializers.ModelSerializer):
    """Сериализатор для статистики публикаций"""

    label = serializers.SerializerMethodField()

    class Meta:
        model = PublicationStats
        fields = ["id", "label", "value", "icon", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_label(self, obj):
        language = self.context.get("language", "ru")
        return getattr(obj, f"label_{language}", obj.label_ru)


class PublicationsPageSerializer(serializers.Serializer):
    """Сериализатор для полной страницы публикаций со статистикой"""

    stats = PublicationStatsSerializer(many=True)
    featured = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()

    def get_featured(self, obj):
        # obj ожидается как словарь с ключом 'featured'
        featured_qs = obj.get("featured", [])
        serializer = PublicationSerializer(featured_qs, many=True, context=self.context)
        return serializer.data

    def get_publications(self, obj):
        pubs_qs = obj.get("publications", [])
        serializer = PublicationSerializer(pubs_qs, many=True, context=self.context)
        return serializer.data




# ==================== SCIENTIFIC PUBLICATION SERIALIZER ====================


class ScientificPublicationSerializer(serializers.ModelSerializer):
    """Сериализатор для раздела 'Научные публикации' (PDF по 3 языкам)"""

    title = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = ScientificPublication
        fields = [
            "id",
            "title",
            "authors",
            "file",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        language = self.context.get("language", "ru")
        return getattr(obj, f"title_{language}", obj.title_ru)

    @extend_schema_field(OpenApiTypes.STR)
    def get_authors(self, obj):
        language = self.context.get("language", "ru")
        return getattr(obj, f"authors_{language}", obj.authors_ru)

    @extend_schema_field(OpenApiTypes.STR)
    def get_file(self, obj):
        language = self.context.get("language", "ru")
        file_field = getattr(obj, f"file_{language}", None)

        if not file_field:
            return None

        try:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(file_field.url)
            return file_field.url
        except Exception:
            return None
