from django.db import models
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _


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
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.section

    def get_content(self, lang="ru"):
        return getattr(self, f"content_{lang}", "")


class EditorialBoard(models.Model):
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)

    file_ru = models.FileField(
        upload_to="editorial_board/",
        blank=True, null=True,
        verbose_name=_("PDF файл (RU)")
    )
    file_en = models.FileField(
        upload_to="editorial_board/",
        blank=True, null=True,
        verbose_name=_("PDF файл (EN)")
    )
    file_kg = models.FileField(
        upload_to="editorial_board/",
        blank=True, null=True,
        verbose_name=_("PDF файл (KG)")
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
    file_ru  = models.FileField(upload_to="archive/ru/", blank=True, null=True, verbose_name=_("PDF (RU)"))
    file_en  = models.FileField(upload_to="archive/en/", blank=True, null=True, verbose_name=_("PDF (EN)"))
    file_kg  = models.FileField(upload_to="archive/kg/", blank=True, null=True, verbose_name=_("PDF (KG)"))
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
    pdf_ru = models.FileField(upload_to="journal/latest/", blank=True, null=True, verbose_name=_("PDF (RU)"))
    pdf_en = models.FileField(upload_to="journal/latest/", blank=True, null=True, verbose_name=_("PDF (EN)"))
    pdf_kg = models.FileField(upload_to="journal/latest/", blank=True, null=True, verbose_name=_("PDF (KG)"))
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