from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import (
    JournalSection,
    EditorialBoard,
    LatestIssue,
    ArchiveYear,
    ArchiveItem,
    EditorialOfficeMember
)
from .serializers import (
    JournalSectionSerializer,
    EditorialBoardSerializer,
    ArchiveYearSerializer,
    LatestIssueSerializer,
    EditorialOfficeMemberSerializer
)

VALID_LANGS = {"ru", "en", "kg"}


def get_lang(request):
    lang = request.query_params.get("lang", "ru")
    return lang if lang in VALID_LANGS else "ru"


class JournalSectionView(generics.ListAPIView):
    queryset = JournalSection.objects.all()
    serializer_class = JournalSectionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = self.request.query_params.get('lang', 'ru')
        return context
    
class EditorialOfficeListView(APIView):
    """GET /api/journal/editorial-office/?lang=ru"""
    def get(self, request):
        lang = request.query_params.get("lang", "ru")
        if lang not in VALID_LANGS:
            return Response(
                {"error": "Invalid lang parameter. Use: ru, en, kg"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        members = EditorialOfficeMember.objects.filter(is_active=True)
        serializer = EditorialOfficeMemberSerializer(
            members, many=True,
            context={"lang": lang, "request": request},
        )
        return Response(serializer.data)


class EditorialOfficeDetailView(APIView):
    def get(self, request, pk):
        lang = request.query_params.get("lang", "ru")
        if lang not in VALID_LANGS:
            return Response(
                {"error": "Invalid lang parameter. Use: ru, en, kg"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            member = EditorialOfficeMember.objects.get(pk=pk, is_active=True)
        except EditorialOfficeMember.DoesNotExist:
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EditorialOfficeMemberSerializer(
            member,
            context={"lang": lang, "request": request},
        )
        return Response(serializer.data)


class EditorialBoardView(APIView):
    def get(self, request):
        lang = get_lang(request)

        board = EditorialBoard.objects.filter(is_active=True).first()

        if not board:
            return Response(
                {"error": "No active editorial board found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EditorialBoardSerializer(
            board,
            context={"lang": lang, "request": request}
        )
        return Response(serializer.data)



class ArchiveListView(APIView):
    """GET /api/journal/archive/?lang=ru — все годы с документами"""
    def get(self, request):
        lang = get_lang(request)
        years = ArchiveYear.objects.filter(is_active=True)
        serializer = ArchiveYearSerializer(
            years, many=True,
            context={"lang": lang, "request": request}
        )
        return Response(serializer.data)


class ArchiveByYearView(APIView):
    """GET /api/journal/archive/{year}/?lang=ru — конкретный год"""
    def get(self, request, year):
        lang = get_lang(request)
        try:
            archive_year = ArchiveYear.objects.get(year=year, is_active=True)
        except ArchiveYear.DoesNotExist:
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArchiveYearSerializer(
            archive_year,
            context={"lang": lang, "request": request}
        )
        return Response(serializer.data)


class LatestIssueView(APIView):
    def get(self, request):
        lang = get_lang(request)
        issues = LatestIssue.objects.filter(is_active=True).order_by("-year")

        if not issues.exists():
            return Response([])

        serializer = LatestIssueSerializer(
            issues,
            many=True,
            context={"language": lang, "request": request}
        )
        return Response(serializer.data)