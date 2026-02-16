from django.db import models
from django.utils.translation import gettext_lazy as _


class AdministrativeStructure(models.Model):
    title_ru = models.CharField(max_length=255, verbose_name=_("Название (RU)"))
    title_en = models.CharField(max_length=255, verbose_name=_("Название (EN)"))
    title_kg = models.CharField(max_length=255, verbose_name=_("Название (KG)"))

    file_ru = models.FileField(
        upload_to="administrative_structure/",
        blank=True, null=True,
        verbose_name=_("PDF файл (RU)")
    )
    file_en = models.FileField(
        upload_to="administrative_structure/",
        blank=True, null=True,
        verbose_name=_("PDF файл (EN)")
    )
    file_kg = models.FileField(
        upload_to="administrative_structure/",
        blank=True, null=True,
        verbose_name=_("PDF файл (KG)")
    )

    is_active = models.BooleanField(default=True, verbose_name=_("Активна"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Административная структура"
        verbose_name_plural = "Административные структуры"

    def __str__(self):
        return self.title_ru