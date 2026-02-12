from django.db import models
from ckeditor.fields import RichTextField


class SportAchievement(models.Model):
    # ФИО спортсмена на трёх языках
    full_name_ru = models.CharField(max_length=255, verbose_name="ФИО (рус)")
    full_name_en = models.CharField(max_length=255, verbose_name="Full Name (en)", blank=True)
    full_name_kg = models.CharField(max_length=255, verbose_name="Аты-жөнү (кырг)", blank=True)

    # Описание достижения на трёх языках (HTML через CKEditor)
    description_ru = RichTextField(verbose_name="Описание достижения (рус)", blank=True)
    description_en = RichTextField(verbose_name="Achievement Description (en)", blank=True)
    description_kg = RichTextField(verbose_name="Жетишкендик сүрөттөмөсү (кырг)", blank=True)

    
    # Активна ли запись
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Спортивное достижение"
        verbose_name_plural = "Спортивные достижения"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name_ru

    def get_description(self, lang="ru"):
        return getattr(self, f"description_{lang}", "")
        return self.description_ru
