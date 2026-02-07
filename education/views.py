from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework import generics

from .models import Master, Phd , CollegeTabCategory, CollegeManagement
from .serializers import (
    MasterSerializer,
    PhdSerializer,
    CollegeDepartmentCategorySerializer,
    CollegeDepartmentCategoryDetailSerializer,
    CollegeManagementSerializer,
)


class CollegeFacultyManagementAPIView(APIView):
    """API для получения руководства факультета (management)

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)
    """

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        # Получаем все активные записи руководства
        items = CollegeManagement.objects.filter(is_active=True).order_by("order")

        serializer = CollegeManagementSerializer(
            items, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeDepartmentCategoriesAPIView(generics.ListAPIView):
    """API для получения списка категорий кафедр"""

    queryset = CollegeTabCategory.objects.filter(is_active=True).order_by("order")
    serializer_class = CollegeDepartmentCategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

    

class CollegeDepartmentCategoryDetailAPIView(APIView):
    """API для получения детальной информации о категории кафедры"""

    def get(self, request, id):
        language = request.query_params.get("lang", "ru")

        try:
            category = (
                CollegeTabCategory.objects.select_related("info")
                .prefetch_related("management")
                .get(id=id, is_active=True)
            )
        except CollegeTabCategory.DoesNotExist:
            return Response(
                {"error": f"Категория с id '{id}' не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CollegeDepartmentCategoryDetailSerializer(
            category, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)




class MasterListAPIView(generics.ListAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

class PhdListAPIView(generics.ListAPIView):
    queryset = Phd.objects.all()
    serializer_class = PhdSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context
