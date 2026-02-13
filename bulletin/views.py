from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import BulletinYear, BulletinIssue
from .serializers import SidebarYearSerializer, BulletinIssueSerializer


def get_lang(request):
   
    lang = request.query_params.get('lang', 'ru')
    if lang not in ('ru', 'en', 'kg'):
        lang = 'ru'
    return lang


class BulletinSidebarView(APIView):
    """
    GET /api/bulletin/sidebar/?lang=ru

    Возвращает все годы со списком выпусков для левого меню.

    Пример ответа:
    [
        {
            "year": 2025,
            "issues": [
                {"id": 1, "number": 1, "description": "<p>...</p>"},
                {"id": 2, "number": 2, "description": "<p>...</p>"}
            ]
        }
    ]
    """
    def get(self, request):
        lang = get_lang(request)
        years = BulletinYear.objects.prefetch_related('issues').all()
        serializer = SidebarYearSerializer(
            years,
            many=True,
            context={'lang': lang}
        )
        return Response(serializer.data)


class BulletinIssueDetailView(APIView):
    """
    GET /api/bulletin/issues/{id}/?lang=ru

    Возвращает один выпуск по его ID.

    Пример ответа:
    {
        "id": 1,
        "year": 2025,
        "issue_number": 1,
        "description": "<p>Полное описание</p>"
    }
    """
    def get(self, request, pk):
        lang = get_lang(request)
        try:
            issue = BulletinIssue.objects.select_related('year').get(pk=pk)
        except BulletinIssue.DoesNotExist:
            return Response(
                {'error': 'Выпуск не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BulletinIssueSerializer(issue, context={'lang': lang})
        return Response(serializer.data)