from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import SportAchievement
from .serializers import SportAchievementSerializer, SportAchievementAdminSerializer


class SportAchievementViewSet(viewsets.ModelViewSet):
    """
    CRUD API для спортивных достижений.

    Поддерживаемые методы:
      GET    /api/sport-achievements/        — список
      GET    /api/sport-achievements/{id}/   — деталь
      POST   /api/sport-achievements/        — создать
      PUT    /api/sport-achievements/{id}/   — обновить
      PATCH  /api/sport-achievements/{id}/   — частично обновить
      DELETE /api/sport-achievements/{id}/   — удалить

    Query-параметры:
      lang=ru|en|kg   — язык ответа (по умолчанию ru)
      is_active=true  — фильтр по активности
    """

    queryset = SportAchievement.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["full_name_ru", "full_name_en", "full_name_kg"]
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return SportAchievementAdminSerializer
        return SportAchievementSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
