from rest_framework.generics import ListAPIView
from .models import (
    StudentSupport,
    StudentsCouncil,
    StudentExchange,
    StudentInstractions,
    ScholarshipProgram,
    ScholarshipRequiredDocument,
)
from .serializers import (
    StudentSupportSerializer,
    StudentsCounseilSerializer,
    StudentExchangeSerializer,
    StudentInstractionsSerializer,
    ScholarshipProgramSerializer,
    ScholarshipRequiredDocumentSerializer,
)


class StudentSupportListAPIView(ListAPIView):
    """API view для поддержки студентов"""
    serializer_class = StudentSupportSerializer
    queryset = StudentSupport.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = self.request.query_params.get('lang', 'ru')
        return context


class StudentsCounseilListAPIView(ListAPIView):
    """API view для студентеческого совета"""
    serializer_class = StudentsCounseilSerializer
    queryset = StudentsCouncil.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = self.request.query_params.get('lang', 'ru')
        return context


class StudentExchangeListAPIView(ListAPIView):
    """API view для программ студентеческого обмена"""
    serializer_class = StudentExchangeSerializer
    queryset = StudentExchange.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = self.request.query_params.get('lang', 'ru')
        return context


class StudentInstractionsListAPIView(ListAPIView):
    """API view для инструкций студентов"""
    serializer_class = StudentInstractionsSerializer
    queryset = StudentInstractions.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = self.request.query_params.get('lang', 'ru')
        return context


class ScholarshipProgramListAPIView(ListAPIView):
    """API view для стипендиальных программ"""
    serializer_class = ScholarshipProgramSerializer
    queryset = ScholarshipProgram.objects.filter(is_active=True).order_by('name_ru')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = self.request.query_params.get('lang', 'ru')
        return context


class ScholarshipRequiredDocumentListAPIView(ListAPIView):
    """API view для документов, требуемых для стипендии"""
    serializer_class = ScholarshipRequiredDocumentSerializer
    queryset = ScholarshipRequiredDocument.objects.all().order_by('scholarship', 'order')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = self.request.query_params.get('lang', 'ru')
        return context
