from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .models import (
    JournalSection,
    EditorialOfficeMember,
    EditorialBoardMember,
    JournalArchive,
    LatestIssue,
)
from .serializers import (
    JournalSectionSerializer,
    EditorialOfficeMemberSerializer,
    EditorialBoardMemberSerializer,
    JournalArchiveSerializer,
    LatestIssueSerializer,
)

VALID_LANGS = {"ru", "en", "kg"}


class JournalSectionView(generics.ListAPIView):
    queryset = JournalSection.objects.all()
    serializer_class = JournalSectionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = self.request.query_params.get('lang', 'ru')
        return context

def get_lang(request):
    lang = request.query_params.get("lang", "ru")
    return lang if lang in VALID_LANGS else "ru"


class EditorialOfficeView(generics.ListAPIView):
    serializer_class = EditorialOfficeMemberSerializer

    def get_queryset(self):
        return EditorialOfficeMember.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = get_lang(self.request)
        return context


class EditorialBoardView(generics.ListAPIView):
    serializer_class = EditorialBoardMemberSerializer

    def get_queryset(self):
        return EditorialBoardMember.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = get_lang(self.request)
        return context

    # Переопределяем list, чтобы вернуть просто список строк
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        lang = get_lang(request)
        names = [obj.get_full_name(lang) for obj in queryset]
        return Response(names)


class JournalArchiveView(generics.ListAPIView):
    serializer_class = JournalArchiveSerializer

    def get_queryset(self):
        return JournalArchive.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = get_lang(self.request)
        return context


class LatestIssueView(APIView):
    def get(self, request):
        lang = get_lang(request)
        issue = LatestIssue.objects.filter(is_active=True).order_by("-year").first()
        if not issue:
            return Response(None)
        serializer = LatestIssueSerializer(
            issue,
            context={"language": lang, "request": request}
        )
        return Response(serializer.data)