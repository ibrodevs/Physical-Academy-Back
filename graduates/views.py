from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import Graduate
from .serializers import GraduateSerializer, GraduateAdminSerializer


class GraduateViewSet(viewsets.ModelViewSet):
    """
    CRUD API для выпускников.

    Поддерживаемые методы:
      GET    /api/graduates/        — список
      GET    /api/graduates/{id}/   — деталь
      POST   /api/graduates/        — создать
      PUT    /api/graduates/{id}/   — обновить
      PATCH  /api/graduates/{id}/   — частично обновить
      DELETE /api/graduates/{id}/   — удалить

    Query-параметры:
      lang=ru|en|kg   — язык ответа (по умолчанию ru)
      is_active=true  — фильтр по активности
    """

    queryset = Graduate.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["full_name_ru", "full_name_en", "full_name_kg"]
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        # При создании/редактировании — принимаем все языки
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return GraduateAdminSerializer
        # При чтении — возвращаем только нужный язык
        return GraduateSerializer

    def get_serializer_context(self):
        """Передаём request в сериализатор, чтобы достать lang из query params."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
