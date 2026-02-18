from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
import os
from django.core.exceptions import ValidationError
from .validators import validate_pdf

# Scientific Direction model
class ScientificDirection(models.Model):
    """Model for scientific research directions"""

    name_ru = models.CharField(_("Name (Russian)"), max_length=255)
    name_en = models.CharField(_("Name (English)"), max_length=255, blank=True)
    name_kg = models.CharField(_("Name (Kyrgyz)"), max_length=255, blank=True)

    description_ru = models.TextField(_("Description (Russian)"))
    description_en = models.TextField(_("Description (English)"), blank=True)
    description_kg = models.TextField(_("Description (Kyrgyz)"), blank=True)

    is_active = models.BooleanField(_("Active"), default=True)
    order = models.IntegerField(_("Order"), default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Scientific Direction")
        verbose_name_plural = _("Scientific Directions")
        ordering = ["order", "name_ru"]

    def __str__(self):
        return self.name_ru

    def get_name(self):
        return self.name_ru

    def get_description(self):
        return self.description_ru


# Dissertation models
class DissertationSpecialization(models.Model):
    """Model for dissertation specializations"""

    code = models.CharField(_("Specialization Code"), max_length=20, default="")
    name_ru = models.CharField(_("Name (Russian)"), max_length=255, default="")
    name_en = models.CharField(
        _("Name (English)"), max_length=255, blank=True, default=""
    )
    name_kg = models.CharField(
        _("Name (Kyrgyz)"), max_length=255, blank=True, default=""
    )

    degree_ru = models.CharField(_("Degree (Russian)"), max_length=100)
    degree_en = models.CharField(_("Degree (English)"), max_length=100, blank=True)
    degree_kg = models.CharField(_("Degree (Kyrgyz)"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("Dissertation Specialization")
        verbose_name_plural = _("Dissertation Specializations")
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name_ru}"

    def get_name(self):
        return self.name_ru

    def get_degree(self):
        return self.degree_ru


class DissertationSecretary(models.Model):
    """Model for dissertation council secretary"""

    name_ru = models.CharField(_("Full Name (Russian)"), max_length=255)
    name_en = models.CharField(_("Full Name (English)"), max_length=255, blank=True)
    name_kg = models.CharField(_("Full Name (Kyrgyz)"), max_length=255, blank=True)

    position_ru = models.CharField(_("Position (Russian)"), max_length=255)
    position_en = models.CharField(_("Position (English)"), max_length=255, blank=True)
    position_kg = models.CharField(_("Position (Kyrgyz)"), max_length=255, blank=True)

    bio_ru = models.TextField(_("Bio (Russian)"))
    bio_en = models.TextField(_("Bio (English)"), blank=True)
    bio_kg = models.TextField(_("Bio (Kyrgyz)"), blank=True)

    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    photo = models.ImageField(
        _("Photo"), upload_to="dissertation/secretary/", blank=True, null=True
    )

    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Dissertation Secretary")
        verbose_name_plural = _("Dissertation Secretaries")

    def __str__(self):
        return self.name_ru

    def get_name(self):
        return self.name_ru

    def get_position(self):
        return self.position_ru

    def get_bio(self):
        return self.bio_ru


class DissertationCouncil(models.Model):
    """Model for dissertation councils"""

    name_ru = models.CharField(_("Name (Russian)"), max_length=255)
    name_en = models.CharField(_("Name (English)"), max_length=255, blank=True)
    name_kg = models.CharField(_("Name (Kyrgyz)"), max_length=255, blank=True)

    description_ru = models.TextField(_("Description (Russian)"))
    description_en = models.TextField(_("Description (English)"), blank=True)
    description_kg = models.TextField(_("Description (Kyrgyz)"), blank=True)

    secretary = models.ForeignKey(
        DissertationSecretary, on_delete=models.PROTECT, related_name="councils"
    )
    specializations = models.ManyToManyField(
        DissertationSpecialization, related_name="councils"
    )

    order_number = models.CharField(_("Order Number"), max_length=50)
    from_date = models.DateField(_("Active From"))
    to_date = models.DateField(_("Active To"))

    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Dissertation Council")
        verbose_name_plural = _("Dissertation Councils")

    def __str__(self):
        return self.name_ru

    def get_name(self):
        return self.name_ru

    def get_description(self):
        return self.description_ru


class DissertationCouncilDocuments(models.Model):
    """Model for dissertation council documents"""

    name_ru = models.CharField(_("Document Name (Russian)"), max_length=255)
    name_en = models.CharField(_("Document Name (English)"), max_length=255, blank=True)
    name_kg = models.CharField(_("Document Name (Kyrgyz)"), max_length=255, blank=True)

    description_ru = models.TextField(_("Description (Russian)"), blank=True)
    description_en = models.TextField(_("Description (English)"), blank=True)
    description_kg = models.TextField(_("Description (Kyrgyz)"), blank=True)

    file = models.FileField(_("Document File"), upload_to="dissertation/documents/")
    is_active = models.BooleanField(_("Active"), default=True)

    council = models.ForeignKey(
        DissertationCouncil,
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Dissertation Council Document")
        verbose_name_plural = _("Dissertation Council Documents")

    def __str__(self):
        return self.name_ru

    def get_name(self):
        return self.name_ru

    def get_description(self):
        return self.description_ru


class VestnikYear(models.Model):
    year = models.IntegerField(_("Year"), unique=True)

    class Meta:
        ordering = ["-year"]
        verbose_name = _("Вестник год")
        verbose_name_plural = _("Вестник годы")

    def __str__(self):
        return str(self.year)

class VestnikRelease(models.Model):
    vestnik_year = models.ForeignKey(
        VestnikYear, on_delete=models.CASCADE, related_name="releases"
    )
    title_ru = models.CharField(_("Title (Russian)"), max_length=255)
    title_en = models.CharField(_("Title (English)"), max_length=255, blank=True)
    title_kg = models.CharField(_("Title (Kyrgyz)"), max_length=255, blank=True)

    description_ru = RichTextUploadingField(_("Description (Russian)"), blank=True)
    description_en = RichTextUploadingField(_("Description (English)"), blank=True)
    description_kg = RichTextUploadingField(_("Description (Kyrgyz)"), blank=True)

    pdf_ru = models.FileField(
        _("PDF File (Russian)"), upload_to="vestnik/releases/", blank=True
    )
    pdf_en = models.FileField(
        _("PDF File (English)"), upload_to="vestnik/releases/", blank=True
    )
    pdf_kg = models.FileField(
        _("PDF File (Kyrgyz)"), upload_to="vestnik/releases/", blank=True
    )

    class Meta:
        ordering = ["-vestnik_year__year"]
        verbose_name = _("Вестник выпуск")
        verbose_name_plural = _("Вестник выпуски")

    def __str__(self):
        return f"{self.title_ru} ({self.vestnik_year.year})"

    def get_title(self, language="ru"):
        return getattr(self, f"title_{language}", self.title_ru)
    
    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)

    def get_pdf(self, language="ru"):
        return getattr(self, f"pdf_{language}", self.pdf_ru)


class DissertationCouncilAdminStaff(models.Model):
    """Model for dissertation council administrative staff members"""

    name_ru = models.CharField(_("Full Name (Russian)"), max_length=255)
    name_en = models.CharField(_("Full Name (English)"), max_length=255, blank=True)
    name_kg = models.CharField(_("Full Name (Kyrgyz)"), max_length=255, blank=True)

    position_ru = models.CharField(_("Position (Russian)"), max_length=255)
    position_en = models.CharField(_("Position (English)"), max_length=255, blank=True)
    position_kg = models.CharField(_("Position (Kyrgyz)"), max_length=255, blank=True)

    bio_ru = models.TextField(_("Bio (Russian)"), blank=True)
    bio_en = models.TextField(_("Bio (English)"), blank=True)
    bio_kg = models.TextField(_("Bio (Kyrgyz)"), blank=True)

    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    photo = models.ImageField(
        _("Photo"), upload_to="dissertation/staff/", blank=True, null=True
    )

    council = models.ForeignKey(
        DissertationCouncil, on_delete=models.CASCADE, related_name="admin_staff"
    )
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Council Admin Staff")
        verbose_name_plural = _("Council Admin Staff")

    def __str__(self):
        return self.name_ru

    def get_name(self):
        return self.name_ru

    def get_position(self):
        return self.position_ru

    def get_bio(self):
        return self.bio_ru

    def get_bio(self):
        return self.bio_ru


# from .nts_committee import (
#     NTSCommitteeRole,
#     NTSResearchDirection,
#     NTSCommitteeMember,
#     NTSCommitteeSection,
# )


class Publication(models.Model):
    """Model for scientific publications"""

    title_ru = models.CharField(_("Title (Russian)"), max_length=500)
    title_en = models.CharField(_("Title (English)"), max_length=500, blank=True)
    title_kg = models.CharField(_("Title (Kyrgyz)"), max_length=500, blank=True)

    author_ru = models.CharField(_("Author (Russian)"), max_length=500, default="")
    author_en = models.CharField(
        _("Author (English)"), max_length=500, blank=True, default=""
    )
    author_kg = models.CharField(
        _("Author (Kyrgyz)"), max_length=500, blank=True, default=""
    )

    journal = models.CharField(_("Journal/Conference"), max_length=255)
    year = models.IntegerField(_("Publication Year"))
    publication_date = models.DateField(_("Publication Date"), null=True, blank=True)
    citation_count = models.IntegerField(_("Citation Count"), default=0)
    impact_factor = models.FloatField(_("Impact Factor"), null=True, blank=True)

    abstract_ru = models.TextField(_("Abstract (Russian)"))
    abstract_en = models.TextField(_("Abstract (English)"), blank=True)
    abstract_kg = models.TextField(_("Abstract (Kyrgyz)"), blank=True)

    doi = models.CharField(_("DOI"), max_length=100, blank=True)
    url = models.URLField(_("External URL"), blank=True)
    pdf_file = models.FileField(_("PDF File"), upload_to="publications/", blank=True)
    image = models.ImageField(
        _("Publication Cover Image"),
        upload_to="publications/images/",
        blank=True,
        null=True,
    )

    publication_type = models.CharField(
        _("Publication Type"),
        max_length=50,
        choices=[
            ("article", _("Journal Article")),
            ("conference", _("Conference Paper")),
            ("book", _("Book/Chapter")),
            ("patent", _("Patent")),
        ],
        default="article",
    )
    is_featured = models.BooleanField(_("Featured"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)
    order = models.IntegerField(_("Order"), default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year", "-order", "title_ru"]
        verbose_name = _("Publication")
        verbose_name_plural = _("Publications")

    def __str__(self):
        return f"{self.title_ru} ({self.year})"

    def get_title(self, language="ru"):
        """Получить заголовок на нужном языке"""
        return getattr(self, f"title_{language}", self.title_ru)

    def get_abstract(self, language="ru"):
        """Получить аннотацию на нужном языке"""
        return getattr(self, f"abstract_{language}", self.abstract_ru)

    def get_authors(self, language="ru"):
        """Получить авторов на нужном языке"""
        return getattr(self, f"author_{language}", self.author_ru)

    def get_journal(self, language="ru"):
        """Получить название журнала (без переводов)"""
        return self.journal


class PublicationTypeOptions:
    """Helper to map publication_type keys to human-readable labels.

    Used by serializers as PublicationTypeOptions(obj.pub_type).label
    """

    _choices = {
        "article": _("Journal Article"),
        "conference": _("Conference Paper"),
        "book": _("Book/Chapter"),
        "patent": _("Patent"),
    }

    def __init__(self, key):
        self.key = key
        self.label = self._choices.get(key, str(key))


class PublicationStats(models.Model):
    """Statistics for publications page"""

    label_ru = models.CharField(_("Label (Russian)"), max_length=255)
    label_en = models.CharField(_("Label (English)"), max_length=255, blank=True)
    label_kg = models.CharField(_("Label (Kyrgyz)"), max_length=255, blank=True)

    value = models.IntegerField(_("Value"))
    icon = models.CharField(_("Icon Class"), max_length=50, blank=True)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = _("Publication Statistic")
        verbose_name_plural = _("Publication Statistics")

    def __str__(self):
        return f"{self.label_ru}: {self.value}"



class DissertationDefense(models.Model):
    """Model for dissertation defense information"""

    title_ru = models.CharField(_("Dissertation Title (Russian)"), max_length=500)
    title_en = models.CharField(
        _("Dissertation Title (English)"), max_length=500, blank=True
    )
    title_kg = models.CharField(
        _("Dissertation Title (Kyrgyz)"), max_length=500, blank=True
    )

    applicant_ru = models.CharField(_("Applicant Name (Russian)"), max_length=255)
    applicant_en = models.CharField(
        _("Applicant Name (English)"), max_length=255, blank=True
    )
    applicant_kg = models.CharField(
        _("Applicant Name (Kyrgyz)"), max_length=255, blank=True
    )

    abstract_ru = models.TextField(_("Abstract (Russian)"))
    abstract_en = models.TextField(_("Abstract (English)"), blank=True)
    abstract_kg = models.TextField(_("Abstract (Kyrgyz)"), blank=True)

    specializations = models.ManyToManyField(
        DissertationSpecialization, related_name="defenses"
    )
    defense_date = models.DateTimeField(_("Defense Date and Time"))

    council = models.ForeignKey(
        DissertationCouncil, on_delete=models.PROTECT, related_name="defenses"
    )

    dissertation_file = models.FileField(
        _("Dissertation File"), upload_to="dissertation/files/", blank=True
    )
    abstract_file = models.FileField(
        _("Abstract File"), upload_to="dissertation/abstracts/", blank=True
    )

    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Dissertation Defense")
        verbose_name_plural = _("Dissertation Defenses")
        ordering = ["-defense_date"]

    def __str__(self):
        return self.title_ru

    def get_title(self):
        return self.title_ru

    def get_applicant(self):
        return self.applicant_ru

    def get_abstract(self):
        return self.abstract_ru


class ConferenceNotice(models.Model):
    """Model for scientific conference announcements"""

    title_ru = models.CharField(_("Conference Title (Russian)"), max_length=500)
    title_en = models.CharField(
        _("Conference Title (English)"), max_length=500, blank=True
    )
    title_kg = models.CharField(
        _("Conference Title (Kyrgyz)"), max_length=500, blank=True
    )

    description_ru = models.TextField(_("Description (Russian)"))
    description_en = models.TextField(_("Description (English)"), blank=True)
    description_kg = models.TextField(_("Description (Kyrgyz)"), blank=True)

    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    registration_deadline = models.DateField(_("Registration Deadline"))

    location = models.CharField(_("Location"), max_length=255)
    organizer = models.CharField(_("Organizer"), max_length=255)

    website = models.URLField(_("Conference Website"), blank=True)
    file = models.FileField(_("Information File"), upload_to="conferences/", blank=True)

    contact_email = models.EmailField(_("Contact Email"), blank=True)
    contact_phone = models.CharField(_("Contact Phone"), max_length=20, blank=True)

    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Conference Notice")
        verbose_name_plural = _("Conference Notices")
        ordering = ["start_date"]

    def __str__(self):
        return self.title_ru

    def get_title(self):
        return self.title_ru

    def get_description(self):
        return self.description_ru




# --- NTS committee models (previously in nts_committee.py) ---
class NTSCommitteeRole(models.Model):
    name_ru = models.CharField("Name (Russian)", max_length=255)
    name_en = models.CharField("Name (English)", max_length=255, blank=True)
    name_kg = models.CharField("Name (Kyrgyz)", max_length=255, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "NTS Committee Role"
        verbose_name_plural = "NTS Committee Roles"
        ordering = ["order", "name_ru"]

    def __str__(self):
        return self.name_ru

    def get_name(self, language="ru"):
        """Get name in specified language"""
        return getattr(self, f"name_{language}", self.name_ru) or self.name_ru


class NTSResearchDirection(models.Model):
    name_ru = models.CharField("Name (Russian)", max_length=255)
    name_en = models.CharField("Name (English)", max_length=255, blank=True)
    name_kg = models.CharField("Name (Kyrgyz)", max_length=255, blank=True)
    description_ru = models.TextField("Description (Russian)", blank=True, default="")
    description_en = models.TextField("Description (English)", blank=True, default="")
    description_kg = models.TextField("Description (Kyrgyz)", blank=True, default="")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "NTS Research Direction"
        verbose_name_plural = "NTS Research Directions"
        ordering = ["order", "name_ru"]

    def __str__(self):
        return self.name_ru

    def get_name(self, language="ru"):
        """Get name in specified language"""
        return getattr(self, f"name_{language}", self.name_ru) or self.name_ru

    def get_description(self, language="ru"):
        """Get description in specified language"""
        return (
            getattr(self, f"description_{language}", self.description_ru)
            or self.description_ru
        )


class NTSCommitteeSection(models.Model):
    section_key = models.CharField(
        "Section Key",
        max_length=100,
        blank=True,
        help_text="Optional stable key for identifying this section (e.g. 'vision', 'mission', 'footer')",
    )
    title_ru = models.CharField("Title (Russian)", max_length=255)
    title_en = models.CharField("Title (English)", max_length=255, blank=True)
    title_kg = models.CharField("Title (Kyrgyz)", max_length=255, blank=True)
    description_ru = models.TextField("Description (Russian)", blank=True)
    description_en = models.TextField("Description (English)", blank=True)
    description_kg = models.TextField("Description (Kyrgyz)", blank=True)
    research_direction = models.ForeignKey(
        NTSResearchDirection, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "NTS Committee Section"
        verbose_name_plural = "NTS Committee Sections"
        ordering = ["order", "title_ru"]

    def __str__(self):
        return self.title_ru

    def get_title(self, language="ru"):
        """Get title in specified language"""
        return (
            getattr(self, f"title_{language}", self.title_ru)
            or self.title_ru
            or self.title_en
            or self.title_kg
            or ""
        )

    def get_description(self, language="ru"):
        """Get description in specified language"""
        return (
            getattr(self, f"description_{language}", self.description_ru)
            or self.description_ru
            or self.description_en
            or self.description_kg
            or ""
        )


class NTSCommitteeMember(models.Model):
    full_name_ru = models.CharField("Full Name (Russian)", max_length=255, default="")
    full_name_en = models.CharField(
        "Full Name (English)", max_length=255, blank=True, default=""
    )
    full_name_kg = models.CharField(
        "Full Name (Kyrgyz)", max_length=255, blank=True, default=""
    )
    role = models.ForeignKey(
        NTSCommitteeRole, on_delete=models.SET_NULL, null=True, blank=True
    )
    section = models.ForeignKey(
        NTSCommitteeSection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )
    bio_ru = models.TextField("Bio (Russian)", blank=True)
    bio_en = models.TextField("Bio (English)", blank=True)
    bio_kg = models.TextField("Bio (Kyrgyz)", blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to="nts/members/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "NTS Committee Member"
        verbose_name_plural = "NTS Committee Members"
        ordering = ["order", "full_name_ru"]

    def __str__(self):
        return self.full_name_ru

    def get_name(self, language="ru"):
        """Get full name in specified language"""
        return (
            getattr(self, f"full_name_{language}", self.full_name_ru)
            or self.full_name_ru
        )

    def get_position(self, language="ru"):
        """Get position from role in specified language"""
        if self.role:
            return self.role.get_name(language)
        return ""

    def get_bio(self, language="ru"):
        """Get bio in specified language"""
        return getattr(self, f"bio_{language}", self.bio_ru) or self.bio_ru


# --- Scopus related models (previously in scopus.py) ---
class ScopusDocumentType(models.Model):
    code = models.CharField(max_length=50, default="")
    label_ru = models.CharField("Label (Russian)", max_length=255, default="")
    label_en = models.CharField(
        "Label (English)", max_length=255, blank=True, default=""
    )
    label_kg = models.CharField(
        "Label (Kyrgyz)", max_length=255, blank=True, default=""
    )

    class Meta:
        verbose_name = "Scopus Document Type"
        verbose_name_plural = "Scopus Document Types"

    def __str__(self):
        return self.label_ru

    def get_label(self, language="ru"):
        """Get label in specified language"""
        return getattr(self, f"label_{language}", self.label_ru)


class ScopusJournal(models.Model):
    title_ru = models.CharField("Title (Russian)", max_length=500, default="")
    title_en = models.CharField(
        "Title (English)", max_length=500, blank=True, default=""
    )
    title_kg = models.CharField(
        "Title (Kyrgyz)", max_length=500, blank=True, default=""
    )
    issn = models.CharField(max_length=50, blank=True, default="")
    publisher = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "Scopus Journal"
        verbose_name_plural = "Scopus Journals"

    def __str__(self):
        return self.title_ru

    def get_title(self, language="ru"):
        """Get title in specified language"""
        return getattr(self, f"title_{language}", self.title_ru)


class ScopusPublisher(models.Model):
    name_ru = models.CharField("Name (Russian)", max_length=255, default="")
    name_en = models.CharField("Name (English)", max_length=255, blank=True, default="")
    name_kg = models.CharField("Name (Kyrgyz)", max_length=255, blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "Scopus Publisher"
        verbose_name_plural = "Scopus Publishers"

    def __str__(self):
        return self.name_ru

    def get_name(self, language="ru"):
        """Get name in specified language"""
        return getattr(self, f"name_{language}", self.name_ru)


class ScopusAuthor(models.Model):
    given_name_ru = models.CharField("Given Name (Russian)", max_length=255, blank=True)
    given_name_en = models.CharField("Given Name (English)", max_length=255, blank=True)
    given_name_kg = models.CharField("Given Name (Kyrgyz)", max_length=255, blank=True)
    family_name_ru = models.CharField(
        "Family Name (Russian)", max_length=255, default=""
    )
    family_name_en = models.CharField(
        "Family Name (English)", max_length=255, blank=True, default=""
    )
    family_name_kg = models.CharField(
        "Family Name (Kyrgyz)", max_length=255, blank=True, default=""
    )
    scopus_id = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Scopus Author"
        verbose_name_plural = "Scopus Authors"

    def __str__(self):
        return f"{self.family_name_ru} {self.given_name_ru}".strip()

    def get_name(self, language="ru"):
        """Get full name in specified language"""
        given = getattr(self, f"given_name_{language}", self.given_name_ru) or ""
        family = getattr(self, f"family_name_{language}", self.family_name_ru) or ""
        return f"{family} {given}".strip()


class ScopusPublication(models.Model):
    title_ru = models.CharField("Title (Russian)", max_length=1000)
    title_en = models.CharField("Title (English)", max_length=1000, blank=True)
    title_kg = models.CharField("Title (Kyrgyz)", max_length=1000, blank=True)
    year = models.IntegerField(null=True, blank=True)
    doi = models.CharField(max_length=200, blank=True)
    journal = models.ForeignKey(
        ScopusJournal, on_delete=models.SET_NULL, null=True, blank=True
    )
    document_type = models.ForeignKey(
        ScopusDocumentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    url = models.URLField(blank=True)
    abstract_ru = models.TextField("Abstract (Russian)", blank=True)
    abstract_en = models.TextField("Abstract (English)", blank=True)
    abstract_kg = models.TextField("Abstract (Kyrgyz)", blank=True)

    class Meta:
        verbose_name = "Scopus Publication"
        verbose_name_plural = "Scopus Publications"

    def __str__(self):
        return self.title_ru


class ScopusPublicationAuthor(models.Model):
    publication = models.ForeignKey(
        ScopusPublication, on_delete=models.CASCADE, related_name="authors"
    )
    author = models.ForeignKey(
        ScopusAuthor, on_delete=models.CASCADE, related_name="publications"
    )
    author_position = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Scopus Publication Author"
        verbose_name_plural = "Scopus Publication Authors"
        ordering = ["author_position"]

    def __str__(self):
        return f"{self.author} - {self.publication}"


class ScopusMetrics(models.Model):
    publication = models.OneToOneField(
        ScopusPublication,
        on_delete=models.CASCADE,
        related_name="metrics",
        null=True,
        blank=True,
    )
    citation_count = models.IntegerField(default=0)
    h_index = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Scopus Metrics"
        verbose_name_plural = "Scopus Metrics"

    def __str__(self):
        return f"Metrics for {self.publication}"


class ScopusStats(models.Model):
    label_ru = models.CharField("Label (Russian)", max_length=255)
    label_en = models.CharField("Label (English)", max_length=255, blank=True)
    label_kg = models.CharField("Label (Kyrgyz)", max_length=255, blank=True)
    value = models.IntegerField()
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Scopus Statistic"
        verbose_name_plural = "Scopus Statistics"
        ordering = ["order"]

    def __str__(self):
        return f"{self.label_ru}: {self.value}"


class ScopusSection(models.Model):
    section_key = models.CharField(
        "Section Key",
        max_length=100,
        blank=True,
        help_text="Optional stable key for identifying this section (e.g. 'header', 'footer')",
    )
    title_ru = models.CharField("Title (Russian)", max_length=255)
    title_en = models.CharField("Title (English)", max_length=255, blank=True)
    title_kg = models.CharField("Title (Kyrgyz)", max_length=255, blank=True)
    description_ru = models.TextField("Description (Russian)", blank=True)
    description_en = models.TextField("Description (English)", blank=True)
    description_kg = models.TextField("Description (Kyrgyz)", blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Scopus Section"
        verbose_name_plural = "Scopus Sections"
        ordering = ["order"]

    def __str__(self):
        return self.title_ru

    def get_title(self):
        return self.title_ru or self.title_en or self.title_kg or ""

    def get_description(self):
        return self.description_ru or self.description_en or self.description_kg or ""


# --- Web of Science models (merged from models/webofscience.py) ---
class WebOfScienceTimeRange(models.Model):
    """Time ranges for Web of Science metrics (e.g., 1 year, 3 years, 5 years)."""

    key = models.CharField(
        _("Key"),
        max_length=50,
        help_text="Unique key for this time range, e.g., '1year', '3years', '5years'",
    )
    title_ru = models.CharField(_("Title (Russian)"), max_length=100)
    title_en = models.CharField(_("Title (English)"), max_length=100, blank=True)
    title_kg = models.CharField(_("Title (Kyrgyz)"), max_length=100, blank=True)
    order = models.IntegerField(_("Order"), default=0)
    is_default = models.BooleanField(_("Is Default"), default=False)

    class Meta:
        verbose_name = _("Web of Science Time Range")
        verbose_name_plural = _("Web of Science Time Ranges")
        ordering = ["order"]

    def __str__(self):
        return self.title_ru

    def get_title(self, language="ru"):
        """Get title in specified language"""
        return (
            getattr(self, f"title_{language}", self.title_ru)
            or self.title_ru
            or self.title_en
            or self.title_kg
            or ""
        )


class WebOfScienceMetric(models.Model):
    """Main metrics for Web of Science (publications, citations, h-index, etc.)."""

    time_range = models.ForeignKey(
        WebOfScienceTimeRange, on_delete=models.CASCADE, related_name="metrics"
    )
    key = models.CharField(
        _("Key"),
        max_length=50,
        help_text="Unique key for this metric, e.g., 'publications', 'citations', 'hindex'",
    )
    value = models.CharField(_("Value"), max_length=50)
    label_ru = models.CharField(_("Label (Russian)"), max_length=100)
    label_en = models.CharField(_("Label (English)"), max_length=100, blank=True)
    label_kg = models.CharField(_("Label (Kyrgyz)"), max_length=100, blank=True)
    description_ru = models.CharField(
        _("Description (Russian)"), max_length=255, blank=True
    )
    description_en = models.CharField(
        _("Description (English)"), max_length=255, blank=True
    )
    description_kg = models.CharField(
        _("Description (Kyrgyz)"), max_length=255, blank=True
    )
    icon = models.CharField(_("Icon"), max_length=20, blank=True)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Web of Science Metric")
        verbose_name_plural = _("Web of Science Metrics")
        ordering = ["time_range", "order"]
        unique_together = ["time_range", "key"]

    def __str__(self):
        return f"{self.label_ru}: {self.value} ({self.time_range})"

    def get_label(self, language="ru"):
        """Get label in specified language"""
        return (
            getattr(self, f"label_{language}", self.label_ru)
            or self.label_ru
            or self.label_en
            or self.label_kg
            or ""
        )

    def get_description(self, language="ru"):
        """Get description in specified language"""
        return (
            getattr(self, f"description_{language}", self.description_ru)
            or self.description_ru
            or self.description_en
            or self.description_kg
            or ""
        )


class WebOfScienceCategory(models.Model):
    """Publication categories for Web of Science (Computer Science, Engineering, etc.)."""

    time_range = models.ForeignKey(
        WebOfScienceTimeRange, on_delete=models.CASCADE, related_name="categories"
    )
    name_ru = models.CharField(_("Name (Russian)"), max_length=100)
    name_en = models.CharField(_("Name (English)"), max_length=100, blank=True)
    name_kg = models.CharField(_("Name (Kyrgyz)"), max_length=100, blank=True)
    count = models.IntegerField(_("Publication Count"))
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Web of Science Category")
        verbose_name_plural = _("Web of Science Categories")
        ordering = ["time_range", "order"]

    def __str__(self):
        return f"{self.name_ru}: {self.count} ({self.time_range})"

    def get_name(self, language="ru"):
        """Get name in specified language"""
        return (
            getattr(self, f"name_{language}", self.name_ru)
            or self.name_ru
            or self.name_en
            or self.name_kg
            or ""
        )


class WebOfScienceCollaboration(models.Model):
    """International collaborations for Web of Science."""

    time_range = models.ForeignKey(
        WebOfScienceTimeRange, on_delete=models.CASCADE, related_name="collaborations"
    )
    country_ru = models.CharField(_("Country (Russian)"), max_length=100)
    country_en = models.CharField(_("Country (English)"), max_length=100, blank=True)
    country_kg = models.CharField(_("Country (Kyrgyz)"), max_length=100, blank=True)
    flag = models.CharField(_("Flag Emoji"), max_length=10, blank=True)
    institutions = models.IntegerField(_("Number of Institutions"))
    publications = models.IntegerField(_("Number of Publications"))
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Web of Science Collaboration")
        verbose_name_plural = _("Web of Science Collaborations")
        ordering = ["time_range", "order"]

    def __str__(self):
        return (
            f"{self.country_ru}: {self.publications} publications ({self.time_range})"
        )

    def get_country(self, language="ru"):
        """Get country name in specified language"""
        return (
            getattr(self, f"country_{language}", self.country_ru)
            or self.country_ru
            or self.country_en
            or self.country_kg
            or ""
        )


class WebOfScienceJournalQuartile(models.Model):
    """Journal quartiles (Q1, Q2, etc.) for Web of Science."""

    time_range = models.ForeignKey(
        WebOfScienceTimeRange,
        on_delete=models.CASCADE,
        related_name="journal_quartiles",
    )
    quartile = models.CharField(_("Quartile"), max_length=10)
    count = models.IntegerField(_("Publication Count"))
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Web of Science Journal Quartile")
        verbose_name_plural = _("Web of Science Journal Quartiles")
        ordering = ["time_range", "order"]

    def __str__(self):
        return f"{self.quartile}: {self.count} ({self.time_range})"


class WebOfScienceAdditionalMetric(models.Model):
    """Additional metrics for Web of Science (avg. citations, hot papers, etc.)."""

    time_range = models.ForeignKey(
        WebOfScienceTimeRange,
        on_delete=models.CASCADE,
        related_name="additional_metrics",
    )
    key = models.CharField(
        _("Key"),
        max_length=50,
        help_text="Unique key for this metric, e.g., 'averageCitations', 'hotPapers'",
    )
    value = models.CharField(_("Value"), max_length=50)
    title_ru = models.CharField(_("Title (Russian)"), max_length=100)
    title_en = models.CharField(_("Title (English)"), max_length=100, blank=True)
    title_kg = models.CharField(_("Title (Kyrgyz)"), max_length=100, blank=True)
    description_ru = models.CharField(
        _("Description (Russian)"), max_length=255, blank=True
    )
    description_en = models.CharField(
        _("Description (English)"), max_length=255, blank=True
    )
    description_kg = models.CharField(
        _("Description (Kyrgyz)"), max_length=255, blank=True
    )
    icon = models.CharField(_("Icon"), max_length=20, blank=True)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Web of Science Additional Metric")
        verbose_name_plural = _("Web of Science Additional Metrics")
        ordering = ["time_range", "order"]
        unique_together = ["time_range", "key"]

    def __str__(self):
        return f"{self.title_ru}: {self.value} ({self.time_range})"

    def get_title(self, language="ru"):
        """Get title in specified language"""
        return (
            getattr(self, f"title_{language}", self.title_ru)
            or self.title_ru
            or self.title_en
            or self.title_kg
            or ""
        )

    def get_description(self, language="ru"):
        """Get description in specified language"""
        return (
            getattr(self, f"description_{language}", self.description_ru)
            or self.description_ru
            or self.description_en
            or self.description_kg
            or ""
        )


class WebOfScienceSection(models.Model):
    """Section text content for Web of Science page (title, subtitle, etc.)."""

    section_key = models.CharField(
        _("Section Key"),
        max_length=100,
        unique=True,
        help_text="Unique key for identifying this section (e.g., 'title', 'subtitle', 'titleIcon')",
    )
    text_ru = models.TextField(_("Text (Russian)"))
    text_en = models.TextField(_("Text (English)"), blank=True)
    text_kg = models.TextField(_("Text (Kyrgyz)"), blank=True)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Web of Science Section")
        verbose_name_plural = _("Web of Science Sections")
        ordering = ["order"]

    def __str__(self):
        return f"{self.section_key}: {self.text_ru[:50]}"

    def get_text(self, language="ru"):
        """Get text in specified language"""
        return (
            getattr(self, f"text_{language}", self.text_ru)
            or self.text_ru
            or self.text_en
            or self.text_kg
            or ""
        )


# --- Student Scientific Society models ---
class StudentScientificSocietyInfo(models.Model):
    """Basic information about the Student Scientific Society."""

    title_ru = models.CharField(_("Title (Russian)"), max_length=255)
    title_en = models.CharField(_("Title (English)"), max_length=255, blank=True)
    title_kg = models.CharField(_("Title (Kyrgyz)"), max_length=255, blank=True)

    subtitle_ru = models.TextField(_("Subtitle (Russian)"))
    subtitle_en = models.TextField(_("Subtitle (English)"), blank=True)
    subtitle_kg = models.TextField(_("Subtitle (Kyrgyz)"), blank=True)

    about_title_ru = models.CharField(_("About Title (Russian)"), max_length=255)
    about_title_en = models.CharField(
        _("About Title (English)"), max_length=255, blank=True
    )
    about_title_kg = models.CharField(
        _("About Title (Kyrgyz)"), max_length=255, blank=True
    )

    about_description_ru = models.TextField(_("About Description (Russian)"))
    about_description_en = models.TextField(
        _("About Description (English)"), blank=True
    )
    about_description_kg = models.TextField(_("About Description (Kyrgyz)"), blank=True)

    projects_title_ru = models.CharField(_("Projects Title (Russian)"), max_length=255)
    projects_title_en = models.CharField(
        _("Projects Title (English)"), max_length=255, blank=True
    )
    projects_title_kg = models.CharField(
        _("Projects Title (Kyrgyz)"), max_length=255, blank=True
    )

    events_title_ru = models.CharField(_("Events Title (Russian)"), max_length=255)
    events_title_en = models.CharField(
        _("Events Title (English)"), max_length=255, blank=True
    )
    events_title_kg = models.CharField(
        _("Events Title (Kyrgyz)"), max_length=255, blank=True
    )

    join_title_ru = models.CharField(_("Join Title (Russian)"), max_length=255)
    join_title_en = models.CharField(
        _("Join Title (English)"), max_length=255, blank=True
    )
    join_title_kg = models.CharField(
        _("Join Title (Kyrgyz)"), max_length=255, blank=True
    )

    leadership_title_ru = models.CharField(
        _("Leadership Title (Russian)"), max_length=255
    )
    leadership_title_en = models.CharField(
        _("Leadership Title (English)"), max_length=255, blank=True
    )
    leadership_title_kg = models.CharField(
        _("Leadership Title (Kyrgyz)"), max_length=255, blank=True
    )

    contacts_title_ru = models.CharField(_("Contacts Title (Russian)"), max_length=255)
    contacts_title_en = models.CharField(
        _("Contacts Title (English)"), max_length=255, blank=True
    )
    contacts_title_kg = models.CharField(
        _("Contacts Title (Kyrgyz)"), max_length=255, blank=True
    )

    upcoming_events_title_ru = models.CharField(
        _("Upcoming Events Title (Russian)"), max_length=255
    )
    upcoming_events_title_en = models.CharField(
        _("Upcoming Events Title (English)"), max_length=255, blank=True
    )
    upcoming_events_title_kg = models.CharField(
        _("Upcoming Events Title (Kyrgyz)"), max_length=255, blank=True
    )

    class Meta:
        verbose_name = _("Student Scientific Society Info")
        verbose_name_plural = _("Student Scientific Society Info")

    def __str__(self):
        return self.title_ru

    def get_title(self, language="ru"):
        return getattr(self, f"title_{language}", self.title_ru)

    def get_subtitle(self, language="ru"):
        return getattr(self, f"subtitle_{language}", self.subtitle_ru)

    def get_about_title(self, language="ru"):
        return getattr(self, f"about_title_{language}", self.about_title_ru)

    def get_about_description(self, language="ru"):
        return getattr(self, f"about_description_{language}", self.about_description_ru)

    def get_projects_title(self, language="ru"):
        return getattr(self, f"projects_title_{language}", self.projects_title_ru)

    def get_events_title(self, language="ru"):
        return getattr(self, f"events_title_{language}", self.events_title_ru)

    def get_join_title(self, language="ru"):
        return getattr(self, f"join_title_{language}", self.join_title_ru)

    def get_leadership_title(self, language="ru"):
        return getattr(self, f"leadership_title_{language}", self.leadership_title_ru)

    def get_contacts_title(self, language="ru"):
        return getattr(self, f"contacts_title_{language}", self.contacts_title_ru)

    def get_upcoming_events_title(self, language="ru"):
        return getattr(
            self, f"upcoming_events_title_{language}", self.upcoming_events_title_ru
        )


class StudentScientificSocietyStat(models.Model):
    """Statistics for Student Scientific Society."""

    label_ru = models.CharField(_("Label (Russian)"), max_length=100)
    label_en = models.CharField(_("Label (English)"), max_length=100, blank=True)
    label_kg = models.CharField(_("Label (Kyrgyz)"), max_length=100, blank=True)
    value = models.CharField(_("Value"), max_length=50)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Student Scientific Society Stat")
        verbose_name_plural = _("Student Scientific Society Stats")
        ordering = ["order"]

    def __str__(self):
        return f"{self.label_ru}: {self.value}"

    def get_label(self, language="ru"):
        return getattr(self, f"label_{language}", self.label_ru)


class StudentScientificSocietyFeature(models.Model):
    """Features in the 'About' section of Student Scientific Society."""

    title_ru = models.CharField(_("Title (Russian)"), max_length=255)
    title_en = models.CharField(_("Title (English)"), max_length=255, blank=True)
    title_kg = models.CharField(_("Title (Kyrgyz)"), max_length=255, blank=True)

    description_ru = models.TextField(_("Description (Russian)"))
    description_en = models.TextField(_("Description (English)"), blank=True)
    description_kg = models.TextField(_("Description (Kyrgyz)"), blank=True)

    icon = models.CharField(
        _("Icon (Emoji)"), max_length=10, help_text="Emoji or icon character"
    )
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Student Scientific Society Feature")
        verbose_name_plural = _("Student Scientific Society Features")
        ordering = ["order"]

    def __str__(self):
        return self.title_ru

    def get_title(self, language="ru"):
        return getattr(self, f"title_{language}", self.title_ru)

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)


class StudentScientificSocietyProject(models.Model):
    """Projects of Student Scientific Society."""

    name_ru = models.CharField(_("Name (Russian)"), max_length=255)
    name_en = models.CharField(_("Name (English)"), max_length=255, blank=True)
    name_kg = models.CharField(_("Name (Kyrgyz)"), max_length=255, blank=True)

    short_description_ru = models.TextField(_("Short Description (Russian)"))
    short_description_en = models.TextField(
        _("Short Description (English)"), blank=True
    )
    short_description_kg = models.TextField(_("Short Description (Kyrgyz)"), blank=True)

    description_ru = models.TextField(_("Description (Russian)"))
    description_en = models.TextField(_("Description (English)"), blank=True)
    description_kg = models.TextField(_("Description (Kyrgyz)"), blank=True)

    icon = models.CharField(
        _("Icon (Emoji)"), max_length=10, help_text="Emoji or icon character"
    )
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Student Scientific Society Project")
        verbose_name_plural = _("Student Scientific Society Projects")
        ordering = ["order"]

    def __str__(self):
        return self.name_ru

    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)

    def get_short_description(self, language="ru"):
        return getattr(self, f"short_description_{language}", self.short_description_ru)

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)


class StudentScientificSocietyProjectTag(models.Model):
    """Tags for Student Scientific Society projects."""

    project = models.ForeignKey(
        StudentScientificSocietyProject, on_delete=models.CASCADE, related_name="tags"
    )
    name_ru = models.CharField(_("Name (Russian)"), max_length=100)
    name_en = models.CharField(_("Name (English)"), max_length=100, blank=True)
    name_kg = models.CharField(_("Name (Kyrgyz)"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("Project Tag")
        verbose_name_plural = _("Project Tags")

    def __str__(self):
        return f"{self.name_ru} - {self.project}"

    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)


class StudentScientificSocietyEvent(models.Model):
    """Events of Student Scientific Society."""

    UPCOMING = "upcoming"
    COMPLETED = "completed"
    STATUS_CHOICES = [
        (UPCOMING, _("Upcoming")),
        (COMPLETED, _("Completed")),
    ]

    name_ru = models.CharField(_("Name (Russian)"), max_length=255)
    name_en = models.CharField(_("Name (English)"), max_length=255, blank=True)
    name_kg = models.CharField(_("Name (Kyrgyz)"), max_length=255, blank=True)

    description_ru = models.TextField(_("Description (Russian)"))
    description_en = models.TextField(_("Description (English)"), blank=True)
    description_kg = models.TextField(_("Description (Kyrgyz)"), blank=True)

    icon = models.CharField(
        _("Icon (Emoji)"), max_length=10, help_text="Emoji or icon character"
    )
    date = models.DateField(_("Event Date"))
    time = models.CharField(
        _("Event Time"),
        max_length=50,
        help_text="Time in text format (e.g. '14:00-16:00')",
    )
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default=UPCOMING
    )
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Student Scientific Society Event")
        verbose_name_plural = _("Student Scientific Society Events")
        ordering = ["date", "order"]

    def __str__(self):
        return self.name_ru

    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)

    def days_left(self):
        from django.utils import timezone

        today = timezone.now().date()
        delta = self.date - today
        return max(0, delta.days)


class StudentScientificSocietyJoinStep(models.Model):
    """Steps to join the Student Scientific Society."""

    step = models.IntegerField(_("Step Number"))
    title_ru = models.CharField(_("Title (Russian)"), max_length=255)
    title_en = models.CharField(_("Title (English)"), max_length=255, blank=True)
    title_kg = models.CharField(_("Title (Kyrgyz)"), max_length=255, blank=True)

    description_ru = models.TextField(_("Description (Russian)"))
    description_en = models.TextField(_("Description (English)"), blank=True)
    description_kg = models.TextField(_("Description (Kyrgyz)"), blank=True)

    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Student Scientific Society Join Step")
        verbose_name_plural = _("Student Scientific Society Join Steps")
        ordering = ["order", "step"]

    def __str__(self):
        return f"Step {self.step}: {self.title_ru}"

    def get_title(self, language="ru"):
        return getattr(self, f"title_{language}", self.title_ru)

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)


class StudentScientificSocietyLeader(models.Model):
    """Leadership of the Student Scientific Society."""

    name_ru = models.CharField(_("Name (Russian)"), max_length=255)
    name_en = models.CharField(_("Name (English)"), max_length=255, blank=True)
    name_kg = models.CharField(_("Name (Kyrgyz)"), max_length=255, blank=True)

    position_ru = models.CharField(_("Position (Russian)"), max_length=255)
    position_en = models.CharField(_("Position (English)"), max_length=255, blank=True)
    position_kg = models.CharField(_("Position (Kyrgyz)"), max_length=255, blank=True)

    department_ru = models.CharField(_("Department (Russian)"), max_length=255)
    department_en = models.CharField(
        _("Department (English)"), max_length=255, blank=True
    )
    department_kg = models.CharField(
        _("Department (Kyrgyz)"), max_length=255, blank=True
    )

    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Student Scientific Society Leader")
        verbose_name_plural = _("Student Scientific Society Leaders")
        ordering = ["order"]

    def __str__(self):
        return self.name_ru

    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)

    def get_position(self, language="ru"):
        return getattr(self, f"position_{language}", self.position_ru)

    def get_department(self, language="ru"):
        return getattr(self, f"department_{language}", self.department_ru)


class StudentScientificSocietyContact(models.Model):
    """Contact information for the Student Scientific Society."""

    label_ru = models.CharField(_("Label (Russian)"), max_length=100)
    label_en = models.CharField(_("Label (English)"), max_length=100, blank=True)
    label_kg = models.CharField(_("Label (Kyrgyz)"), max_length=100, blank=True)

    value = models.CharField(_("Value"), max_length=255)
    icon = models.CharField(
        _("Icon (Emoji)"), max_length=10, help_text="Emoji or icon character"
    )
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Student Scientific Society Contact")
        verbose_name_plural = _("Student Scientific Society Contacts")
        ordering = ["order"]

    def __str__(self):
        return f"{self.label_ru}: {self.value}"

    def get_label(self, language="ru"):
        return getattr(self, f"label_{language}", self.label_ru)



    def validate_pdf(file):
        ext = os.path.splitext(file.name)[1]
        if ext.lower() != ".pdf":
            raise ValidationError("Разрешены только PDF файлы.")

        if file.size > 20 * 1024 * 1024:
            raise ValidationError("Размер файла не должен превышать 20MB.")


class ScientificPublication(models.Model):
    """Model for scientific publications with 3-language PDF support"""

    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)

    authors_ru = models.CharField(max_length=255)
    authors_en = models.CharField(max_length=255)
    authors_kg = models.CharField(max_length=255)

    # PDF files
    file_ru = models.FileField(
        upload_to="scientific_publications/",
        validators=[validate_pdf],
        blank=True,
        null=True,
        verbose_name="PDF (RU)",
    )

    file_en = models.FileField(
        upload_to="scientific_publications/",
        validators=[validate_pdf],
        blank=True,
        null=True,
        verbose_name="PDF (EN)",
    )

    file_kg = models.FileField(
        upload_to="scientific_publications/",
        validators=[validate_pdf],
        blank=True,
        null=True,
        verbose_name="PDF (KG)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Scientific Publication"
        verbose_name_plural = "Scientific Publications"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title_ru


