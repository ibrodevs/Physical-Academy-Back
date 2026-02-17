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


class EditorialOfficeMember(models.Model):
    full_name_ru = models.CharField(max_length=255)
    full_name_en = models.CharField(max_length=255)
    full_name_kg = models.CharField(max_length=255)
    position_ru = models.CharField(max_length=255)
    position_en = models.CharField(max_length=255)
    position_kg = models.CharField(max_length=255)
    photo = CloudinaryField(blank=True, null=True, verbose_name=_("Фото"))
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.full_name_ru

    def get_full_name(self, lang="ru"):
        return getattr(self, f"full_name_{lang}", "")

    def get_position(self, lang="ru"):
        return getattr(self, f"position_{lang}", "")


class EditorialBoardMember(models.Model):
    full_name_ru = models.CharField(max_length=255)
    full_name_en = models.CharField(max_length=255)
    full_name_kg = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.full_name_ru

    def get_full_name(self, lang="ru"):
        return getattr(self, f"full_name_{lang}", "")


class JournalArchive(models.Model):
    year = models.PositiveIntegerField()
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)
    pdf_ru = models.FileField(upload_to="journal/archive/", blank=True, null=True, verbose_name=_("PDF (RU)"))
    pdf_en = models.FileField(upload_to="journal/archive/", blank=True, null=True, verbose_name=_("PDF (EN)"))
    pdf_kg = models.FileField(upload_to="journal/archive/", blank=True, null=True, verbose_name=_("PDF (KG)"))
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return f"{self.title_ru} ({self.year})"

    def get_title(self, lang="ru"):
        return getattr(self, f"title_{lang}", "")

    def get_pdf(self, lang="ru"):
        return getattr(self, f"pdf_{lang}", None)


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
        return getattr(self, f"pdf_{lang}", None)