from rest_framework import serializers
from .models import (
    JournalSection,
    EditorialBoard,
    LatestIssue,
    ArchiveYear,
    ArchiveItem,
    EditorialOfficeMember
)


class JournalSectionSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model  = JournalSection
        fields = ("section", "content")

    def get_content(self, obj):
        lang = self.context.get("language", "ru")
        return obj.get_content(lang)
    

class EditorialOfficeMemberSerializer(serializers.ModelSerializer):
    name        = serializers.SerializerMethodField()
    position    = serializers.SerializerMethodField()
    image       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model  = EditorialOfficeMember
        fields = ["id", "name", "position", "image", "description"]

    def _lang(self):
        return self.context.get("lang", "ru")

    def get_name(self, obj):
        return getattr(obj, f"name_{self._lang()}", obj.name_ru)

    def get_position(self, obj):
        return getattr(obj, f"position_{self._lang()}", obj.position_ru)

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_description(self, obj):
        return getattr(obj, f"description_{self._lang()}", obj.description_ru)


class EditorialBoardSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    pdf   = serializers.SerializerMethodField()

    class Meta:
        model  = EditorialBoard
        fields = ["title", "pdf", "updated_at"]

    def get_title(self, obj):
        lang = self.context.get("lang", "ru")
        return getattr(obj, f"title_{lang}", obj.title_ru)

    def get_pdf(self, obj):
        request = self.context.get("request")
        lang    = self.context.get("lang", "ru")
        file    = getattr(obj, f"file_{lang}", None)
        if file and request:
            return request.build_absolute_uri(file.url)
        return None



class ArchiveItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    pdf   = serializers.SerializerMethodField()

    class Meta:
        model  = ArchiveItem
        fields = ["id", "title", "pdf"]

    def get_title(self, obj):
        lang = self.context.get("lang", "ru")
        return getattr(obj, f"title_{lang}", obj.title_ru)

    def get_pdf(self, obj):
        request = self.context.get("request")
        lang    = self.context.get("lang", "ru")
        file    = getattr(obj, f"file_{lang}", None)
        if file and file.name and request:
            return request.build_absolute_uri(file.url)
        return None


class ArchiveYearSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model  = ArchiveYear
        fields = ["year", "items"]

    def get_items(self, obj):
        docs = obj.items.filter(is_active=True).order_by("sort_order", "id")
        return ArchiveItemSerializer(docs, many=True, context=self.context).data


class LatestIssueSerializer(serializers.ModelSerializer):
    title    = serializers.SerializerMethodField()
    pdf_file = serializers.SerializerMethodField()

    class Meta:
        model  = LatestIssue
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