from rest_framework import serializers
from .models import AdministrativeStructure


class AdministrativeStructureSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    pdf_file = serializers.SerializerMethodField()

    class Meta:
        model = AdministrativeStructure
        fields = ["id", "title", "pdf_file"]

    def get_title(self, obj):
        request = self.context.get("request")
        lang = request.query_params.get("lang", "ru") if request else "ru"
        if lang == "en":
            return obj.title_en
        elif lang == "kg":
            return obj.title_kg
        return obj.title_ru

    def get_pdf_file(self, obj):
        request = self.context.get("request")
        lang = request.query_params.get("lang", "ru") if request else "ru"
        if lang == "en":
            file_field = obj.file_en
        elif lang == "kg":
            file_field = obj.file_kg
        else:
            file_field = obj.file_ru

        if file_field and hasattr(file_field, "url"):
            return request.build_absolute_uri(file_field.url) if request else file_field.url
        return None