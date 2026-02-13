from django.db import models
from ckeditor.fields import RichTextField


class BulletinYear(models.Model):

    year = models.PositiveIntegerField(
        unique=True,          # нельзя создать два одинаковых года
        verbose_name="Год"
    )

    class Meta:
        ordering = ['-year']  # сначала показываем свежие годы (2025, 2024...)
        verbose_name = "Год вестника"
        verbose_name_plural = "Годы вестника"

    def __str__(self):
        return str(self.year)


class BulletinIssue(models.Model):
 
    year = models.ForeignKey(
        BulletinYear,
        related_name='issues',     # через year.issues.all() получаем все выпуски года
        on_delete=models.CASCADE,  # если удалить год — удалятся все его выпуски
        verbose_name="Год"
    )
    issue_number = models.PositiveIntegerField(
        verbose_name="Номер выпуска"
    )

    # Описание на трёх языках — через редактор CKEditor (поддерживает HTML)
    description_ru = RichTextField(verbose_name="Описание (Русский)")
    description_en = RichTextField(verbose_name="Описание (English)")
    description_kg = RichTextField(verbose_name="Описание (Кыргызча)")

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        unique_together = ('year', 'issue_number')  # нельзя создать два №1 за один год
        ordering = ['issue_number']                  # выпуски по порядку номеров
        verbose_name = "Выпуск вестника"
        verbose_name_plural = "Выпуски вестника"

    def __str__(self):
        return f"{self.year.year} — №{self.issue_number}"