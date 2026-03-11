from django.db import models
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import os


APP_MAX_FILE_SIZE_MB = int(os.getenv("JOURNAL_MAX_FILE_SIZE_MB", "50"))
# Cloudinary may enforce a lower hard cap on the account/preset level.
CLOUDINARY_HARD_CAP_MB = int(os.getenv("CLOUDINARY_HARD_CAP_MB", "10"))
EFFECTIVE_MAX_FILE_SIZE_MB = min(APP_MAX_FILE_SIZE_MB, CLOUDINARY_HARD_CAP_MB)
EFFECTIVE_MAX_FILE_SIZE_BYTES = EFFECTIVE_MAX_FILE_SIZE_MB * 1024 * 1024


def validate_file_size_50mb(value):
    if not value:
        return
    if value.size > EFFECTIVE_MAX_FILE_SIZE_BYTES:
        raise ValidationError(
            _("Максимальный размер файла: %(max_size)s MB."),
            params={"max_size": EFFECTIVE_MAX_FILE_SIZE_MB},
        )


class JournalSection(models.Model):
    SECTION_CHOICES = (
        ("about",        "About the Journal"),
        ("aims",         "Aims and Scope"),
        ("guidelines",   "Guidelines for Authors"),
        ("requirements", "Author Requirements"),
        ("indexing",     "Indexing and Abstracting"),
        ("ethics",       "Publication Ethics"),
        ("contacts",     "Contact Information"),
    )

    section    = models.CharField(max_length=30, choices=SECTION_CHOICES, unique=True)
    content_ru = RichTextField()
    content_en = RichTextField()
    content_kg = RichTextField()
    pdf_ru = models.FileField(
        upload_to="journal/sections/",
        blank=True,
        null=True,
        verbose_name=_("PDF (RU)"),
        validators=[validate_file_size_50mb],
    )
    pdf_en = models.FileField(
        upload_to="journal/sections/",
        blank=True,
        null=True,
        verbose_name=_("PDF (EN)"),
        validators=[validate_file_size_50mb],
    )
    pdf_kg = models.FileField(
        upload_to="journal/sections/",
        blank=True,
        null=True,
        verbose_name=_("PDF (KG)"),
        validators=[validate_file_size_50mb],
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.section

    def get_content(self, lang="ru"):
        return getattr(self, f"content_{lang}", "")


class EditorialOfficeMember(models.Model):

    name_ru = models.CharField(max_length=255, verbose_name=_("ФИО (RU)"))
    name_en = models.CharField(max_length=255, verbose_name=_("ФИО (EN)"))
    name_kg = models.CharField(max_length=255, verbose_name=_("ФИО (KG)"))

    position_ru = models.CharField(max_length=255, verbose_name=_("Должность (RU)"))
    position_en = models.CharField(max_length=255, verbose_name=_("Должность (EN)"))
    position_kg = models.CharField(max_length=255, verbose_name=_("Должность (KG)"))

    image = models.ImageField(
        upload_to="journal/editorial_office/",
        blank=True, null=True,
        verbose_name=_("Фото"),
    )

    description_ru = RichTextField(blank=True, default="", verbose_name=_("Описание (RU)"))
    description_en = RichTextField(blank=True, default="", verbose_name=_("Описание (EN)"))
    description_kg = RichTextField(blank=True, default="", verbose_name=_("Описание (KG)"))

    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Порядок"))
    is_active  = models.BooleanField(default=True, verbose_name=_("Активен"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = _("Член редакции")
        verbose_name_plural = _("Редакция журнала")

    def __str__(self):
        return self.name_ru


class EditorialBoard(models.Model):
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)

    file_ru = models.FileField(
        upload_to="editorial_board/",
        blank=True, null=True,
        verbose_name=_("PDF файл (RU)"),
        validators=[validate_file_size_50mb],
    )
    file_en = models.FileField(
        upload_to="editorial_board/",
        blank=True, null=True,
        verbose_name=_("PDF файл (EN)"),
        validators=[validate_file_size_50mb],
    )
    file_kg = models.FileField(
        upload_to="editorial_board/",
        blank=True, null=True,
        verbose_name=_("PDF файл (KG)"),
        validators=[validate_file_size_50mb],
    )

    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Редколлегия"
        verbose_name_plural = "Редколлегия"

    def __str__(self):
        return self.title_ru
    


class ArchiveYear(models.Model):
    year      = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return str(self.year)


class ArchiveItem(models.Model):
    year     = models.ForeignKey(ArchiveYear, on_delete=models.CASCADE, related_name="items")
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)
    file_ru  = models.FileField(
        upload_to="archive/ru/",
        blank=True,
        null=True,
        verbose_name=_("PDF (RU)"),
        validators=[validate_file_size_50mb],
    )
    file_en  = models.FileField(
        upload_to="archive/en/",
        blank=True,
        null=True,
        verbose_name=_("PDF (EN)"),
        validators=[validate_file_size_50mb],
    )
    file_kg  = models.FileField(
        upload_to="archive/kg/",
        blank=True,
        null=True,
        verbose_name=_("PDF (KG)"),
        validators=[validate_file_size_50mb],
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title_ru


class LatestIssue(models.Model):
    year = models.PositiveIntegerField()
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)
    pdf_ru = models.FileField(
        upload_to="journal/latest/",
        blank=True,
        null=True,
        verbose_name=_("PDF (RU)"),
        validators=[validate_file_size_50mb],
    )
    pdf_en = models.FileField(
        upload_to="journal/latest/",
        blank=True,
        null=True,
        verbose_name=_("PDF (EN)"),
        validators=[validate_file_size_50mb],
    )
    pdf_kg = models.FileField(
        upload_to="journal/latest/",
        blank=True,
        null=True,
        verbose_name=_("PDF (KG)"),
        validators=[validate_file_size_50mb],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return f"{self.title_ru} ({self.year})"

    def get_title(self, lang="ru"):
        return getattr(self, f"title_{lang}", "")

    def get_pdf(self, lang="ru"):
     field = getattr(self, f"pdf_{lang}", None)
     return field if field else None

class ThemeRegistry(models.Model):
    title_ru = models.CharField(max_length=255, verbose_name=_("Название темы (RU)"))
    title_en = models.CharField(max_length=255, verbose_name=_("Название темы (EN)"))
    title_kg = models.CharField(max_length=255, verbose_name=_("Название темы (KG)"))

    pdf_ru = models.FileField(upload_to="Journal/themes/", blank=True, null=True, verbose_name=_("PDF (RU)"))
    pdf_en = models.FileField(upload_to="Journal/themes/", blank=True, null=True, verbose_name=_("PDF (EN)"))
    pdf_kg = models.FileField(upload_to="Journal/themes/", blank=True, null=True, verbose_name=_("PDF (KG)"))

    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Порядок"))
    is_active  = models.BooleanField(default=True, verbose_name=_("Активна"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = _("Реестр тем")
        verbose_name_plural = _("Реестр тем")

    def __str__(self):
        return self.title_ru
    

class Regulation(models.Model):
    title_ru = models.CharField(max_length=255, verbose_name=_("Название (RU)"))
    title_en = models.CharField(max_length=255, verbose_name=_("Название (EN)"))
    title_kg = models.CharField(max_length=255, verbose_name=_("Название (KG)"))

    pdf_ru = models.FileField(upload_to="Journal/regulations/", blank=True, null=True, verbose_name=_("PDF (RU)"))
    pdf_en = models.FileField(upload_to="Journal/regulations/", blank=True, null=True, verbose_name=_("PDF (EN)"))
    pdf_kg = models.FileField(upload_to="Journal/regulations/", blank=True, null=True, verbose_name=_("PDF (KG)"))

    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Порядок"))
    is_active  = models.BooleanField(default=True, verbose_name=_("Активна"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = _("Положение")
        verbose_name_plural = _("Положения")

    def __str__(self):
        return self.title_ru