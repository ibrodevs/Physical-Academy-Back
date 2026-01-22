from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import (
    TabCategory,
    Card,
    TimelineEvent,
    AboutCollege,
    Management,
    Teacher,
    Specialization,
    Department,
    DepartmentStaff,
    GalleryCard,
    MissionStrategy
)


class GalleryCardSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryCard
        fields = ["id", "title", "description", "photo", ]

    def get_title(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_title(language)
    
    def get_description(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_description(language)
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_photo(self, obj) -> str | None:
        img = getattr(obj, "photo", None)
        if not img:
            return None
        try:
            return img.url
        except Exception:
            return str(img)

class CardSerializer(serializers.ModelSerializer):
    """Сериализатор для карточек"""

    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ["id", "title", "description", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_title(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_description(language)


class TimelineEventSerializer(serializers.ModelSerializer):
    """Сериализатор для событий истории"""

    image = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        model = TimelineEvent
        fields = ["id", "image", "event", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_event(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_event(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_image(self, obj) -> str:
        if not obj.image:
            return None

        try:
            return obj.image.url
        except Exception:
            return str(obj.image)


class TabCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий/табов"""

    title = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    class Meta:
        model = TabCategory
        fields = ["id", "key", "title", "icon", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_title(language)
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_icon(self, obj) -> str | None:
        img = getattr(obj, "icon", None)
        if not img:
            return None
        try:
            return img.url
        except Exception:
            return str(img)


class CollegeDataSerializer(serializers.Serializer):
    """Общий сериализатор для всех данных колледжа"""

    tabs = TabCategorySerializer(many=True)


class AboutCollegeSerializer(serializers.ModelSerializer):
    """Сериализатор для текста 'О колледже'"""

    text = serializers.SerializerMethodField()

    class Meta:
        model = AboutCollege
        fields = ["id", "text", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_text(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_text(language)


class ManagementSerializer(serializers.ModelSerializer):
    """Сериализатор для руководства колледжа"""

    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    class Meta:
        model = Management
        fields = ["id", "name", "role", "photo", "phone", "email", "resume", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_name(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_role(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_role(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_photo(self, obj) -> str | None:
        img = getattr(obj, "photo", None)
        if not img:
            return None
        try:
            return img.url
        except Exception:
            return str(img)

    @extend_schema_field(OpenApiTypes.STR)
    def get_resume(self, obj) -> str | None:
        if not obj.resume:
            return None
        try:
            return obj.resume.url
        except Exception:
            return str(obj.resume)



class TeacherSerializer(serializers.ModelSerializer):
    """Сериализатор для преподавателей колледжа"""

    name = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ["id", "name", "subject", "photo", "phone", "email", "resume", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_name(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_subject(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_subject(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_photo(self, obj) -> str | None:
        img = getattr(obj, "photo", None)
        if not img:
            return None
        try:
            return img.url
        except Exception:
            return str(img)

    @extend_schema_field(OpenApiTypes.STR)
    def get_resume(self, obj) -> str | None:
        if not obj.resume:
            return None
        try:
            return obj.resume.url
        except Exception:
            return str(obj.resume)



class SpecializationSerializer(serializers.ModelSerializer):
    """Сериализатор для специализаций колледжа"""

    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Specialization
        fields = ["id", "title", "description", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_title(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_description(language)


class DepartmentStaffSerializer(serializers.ModelSerializer):
    """Сериализатор для сотрудников кафедры"""

    name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentStaff
        fields = ["id", "name", "position", "resume", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_name(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_position(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_position(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_resume(self, obj) -> str | None:
        if not obj.resume:
            return None
        try:
            return obj.resume.url
        except Exception:
            return str(obj.resume)

class DepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор для кафедр колледжа"""

    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    staff = DepartmentStaffSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "description", "staff", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_name(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_description(language)


class MissionStrategySerializer(serializers.ModelSerializer):
    """Сериализатор для миссий и стратегий колледжа"""

    title = serializers.SerializerMethodField()
    pdf_ru = serializers.SerializerMethodField()
    pdf_kg = serializers.SerializerMethodField()
    pdf_en = serializers.SerializerMethodField()

    class Meta:
        model = MissionStrategy
        fields = ["id", "title", "pdf_ru", "pdf_kg", "pdf_en", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_title(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_pdf_ru(self, obj) -> str | None:
        if not obj.pdf_ru:
            return None
        try:
            return obj.pdf_ru.url
        except Exception:
            return str(obj.pdf_ru)

    @extend_schema_field(OpenApiTypes.STR)
    def get_pdf_kg(self, obj) -> str | None:
        if not obj.pdf_kg:
            return None
        try:
            return obj.pdf_kg.url
        except Exception:
            return str(obj.pdf_kg)

    @extend_schema_field(OpenApiTypes.STR)
    def get_pdf_en(self, obj) -> str | None:
        if not obj.pdf_en:
            return None
        try:
            return obj.pdf_en.url
        except Exception:
            return str(obj.pdf_en)