from rest_framework import serializers
from .models import SportAchievement


class SportAchievementSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = SportAchievement
        fields = ["id", "full_name", "description", "is_active"]

    def _get_lang(self):
        """Получаем язык из query-параметра. По умолчанию — ru."""
        request = self.context.get("request")
        if request:
            lang = request.query_params.get("lang", "ru")
            if lang not in ["ru", "en", "kg"]:
                lang = "ru"
            return lang
        return "ru"

    def get_full_name(self, instance):
        lang = self._get_lang()
        # Fallback: если выбранный язык пустой — возвращаем ru
        value = getattr(instance, f"full_name_{lang}", "") or instance.full_name_ru
        return value

    def get_description(self, instance):
        lang = self._get_lang()
        value = getattr(instance, f"description_{lang}", "") or instance.description_ru
        return value


class SportAchievementAdminSerializer(serializers.ModelSerializer):
    """Полный сериализатор для создания/редактирования (все языки)."""

    class Meta:
        model = SportAchievement
        fields = "__all__"


       
