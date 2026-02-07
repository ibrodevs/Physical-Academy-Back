from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import (
    StudentSupport,
    StudentsCouncil,
    StudentExchange,
    StudentInstractions,
    ScholarshipProgram,
    ScholarshipRequiredDocument,
)


class StudentSupportSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = StudentSupport
        fields = ['id', 'text']

    @extend_schema_field(OpenApiTypes.STR)
    def get_text(self, obj):
        text = obj.get_text(lang=self.context.get('language', 'ru'))
        if text:
            return str(text)
        return None


class StudentsCounseilSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = StudentsCouncil
        fields = ['id', 'text']

    @extend_schema_field(OpenApiTypes.STR)
    def get_text(self, obj):
        text = obj.get_text(lang=self.context.get('language', 'ru'))
        if text:
            return str(text)
        return None


class StudentExchangeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = StudentExchange
        fields = ['id', 'name', 'desc', 'photo']

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        return obj.get_name(lang=self.context.get('language', 'ru'))

    @extend_schema_field(OpenApiTypes.STR)
    def get_desc(self, obj):
        return obj.get_desc(lang=self.context.get('language', 'ru'))

    @extend_schema_field(OpenApiTypes.STR)
    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None


class StudentInstractionsSerializer(serializers.ModelSerializer):
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = StudentInstractions
        fields = ['id', 'pdf']

    @extend_schema_field(OpenApiTypes.STR)
    def get_pdf(self, obj):
        pdf_file = obj.get_pdf(lang=self.context.get('language', 'ru'))
        if pdf_file and hasattr(pdf_file, 'url'):
            return pdf_file.url
        return str(pdf_file) if pdf_file else None


class ScholarshipRequiredDocumentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ScholarshipRequiredDocument
        fields = ['id', 'name', 'description', 'is_required', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        return obj.get_field('name', language=self.context.get('language', 'ru'))

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        desc = obj.get_field('description', language=self.context.get('language', 'ru'))
        return desc if desc else None


class ScholarshipProgramSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    eligibility_criteria = serializers.SerializerMethodField()
    required_documents = ScholarshipRequiredDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ScholarshipProgram
        fields = [
            'id',
            'name',
            'description',
            'eligibility_criteria',
            'amount',
            'currency',
            'application_deadline',
            'application_link',
            'contact_email',
            'contact_phone',
            'is_active',
            'required_documents',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        return obj.get_field('name', language=self.context.get('language', 'ru'))

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        return obj.get_field('description', language=self.context.get('language', 'ru'))

    @extend_schema_field(OpenApiTypes.STR)
    def get_eligibility_criteria(self, obj):
        return obj.get_field(
            'eligibility_criteria', language=self.context.get('language', 'ru')
        )
