from django.db import models
from ckeditor.fields import RichTextField


class Graduate(models.Model):
    # ФИО на трёх языках
    full_name_ru = models.CharField(max_length=255, verbose_name="ФИО (рус)")
    full_name_en = models.CharField(max_length=255, verbose_name="Full Name (en)", blank=True)
    full_name_kg = models.CharField(max_length=255, verbose_name="Аты-жөнү (кырг)", blank=True)

    # Описание на трёх языках (HTML через CKEditor)
    description_ru = RichTextField(verbose_name="Описание (рус)", blank=True)
    description_en = RichTextField(verbose_name="Description (en)", blank=True)
    description_kg = RichTextField(verbose_name="Сүрөттөмө (кырг)", blank=True)

    # Активен ли выпускник
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Выпускник"
        verbose_name_plural = "Выпускники"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name_ru
