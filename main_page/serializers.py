from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import (
    AcademyInfrastructure,
    AcademyStatistics,
    AcademyAchievements,
    Accreditation,
    Mission,
    aboutStatistics,
    AboutPhotos,
    History
)


class HistorySerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ["id", "text", "image_url"]

    def get_text(self, obj):
        return obj.get_text(self.context.get("language", "ru"))
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_image_url(self, obj):
        if not obj.image:
            return None
        try:
            return obj.image.url
        except Exception:
            return str(obj.image)

class AboutStatisticsSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = aboutStatistics
        fields = ["id", "titleInt", "description", "emoji"]

    def get_description(self, obj):
        return obj.get_description(self.context.get("language", "ru"))


class AboutPhotosSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = AboutPhotos
        fields = ["id", "photo", "description"]

    def get_description(self, obj):
        return obj.get_description(self.context.get("language", "ru"))




class MissionSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = Mission
        fields = ["id", "pdf", "title", "description"]

    def get_title(self, obj):
        return obj.get_title(self.context.get("language", "ru"))

    def get_description(self, obj):
        return obj.get_description(self.context.get("language", "ru"))

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
        



class AccreditationSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = Accreditation
        fields = [
            "name",
            "description",
            "pdf",
        ]

    def get_description(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_description(lang)

    def get_name(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_name(lang)

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
        

class AcademyStatisticsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = AcademyStatistics
        fields = ["id", "title", "description", "titleInt"]

    def get_title(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_title(lang)

    def get_description(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_description(lang)


class AcademyAchievementsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = AcademyAchievements
        fields = [
            "title",
            "description",
            "year",
        ]

    def get_title(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_title(lang)

    def get_description(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_description(lang)


class AcademyInfrastructureSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = AcademyInfrastructure
        fields = ["id", "titleInt", "description", "emoji"]

    def get_description(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_description(lang)
