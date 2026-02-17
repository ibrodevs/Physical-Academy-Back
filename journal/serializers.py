from rest_framework import serializers
from .models import (
    JournalSection,
    EditorialOfficeMember,
    EditorialBoardMember,
    JournalArchive,
    LatestIssue,
)


class JournalSectionSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model  = JournalSection
        fields = ("section", "content")

    def get_content(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_content(lang)



from rest_framework import serializers
from .models import (
    EditorialOfficeMember,
    EditorialBoardMember,
    JournalArchive,
    LatestIssue,
)


class EditorialOfficeMemberSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = EditorialOfficeMember
        fields = ("full_name", "position", "photo")

    def get_lang(self):
        return self.context.get("language", "ru")

    def get_full_name(self, obj):
        return obj.get_full_name(self.get_lang())

    def get_position(self, obj):
        return obj.get_position(self.get_lang())

    def get_photo(self, obj):
        request = self.context.get("request")
        if obj.photo:
            # Cloudinary возвращает URL напрямую
            return obj.photo.url
        return None


class EditorialBoardMemberSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = EditorialBoardMember
        fields = ("full_name",)

    def get_full_name(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_full_name(lang)


class JournalArchiveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    pdf_file = serializers.SerializerMethodField()

    class Meta:
        model = JournalArchive
        fields = ("year", "title", "pdf_file")

    def get_lang(self):
        return self.context.get("language", "ru")

    def get_title(self, obj):
        return obj.get_title(self.get_lang())

    def get_pdf_file(self, obj):
        request = self.context.get("request")
        pdf = obj.get_pdf(self.get_lang())
        if pdf and hasattr(pdf, 'url'):
            return request.build_absolute_uri(pdf.url) if request else pdf.url
        return None


class LatestIssueSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    pdf_file = serializers.SerializerMethodField()

    class Meta:
        model = LatestIssue
        fields = ("year", "title", "pdf_file")

    def get_lang(self):
        return self.context.get("language", "ru")

    def get_title(self, obj):
        return obj.get_title(self.get_lang())

    def get_pdf_file(self, obj):
        request = self.context.get("request")
        pdf = obj.get_pdf(self.get_lang())
        if pdf and hasattr(pdf, 'url'):
            return request.build_absolute_uri(pdf.url) if request else pdf.url
        return None