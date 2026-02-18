from django.contrib import admin
from .models import (
    NTSCommitteeRole,
    NTSResearchDirection,
    NTSCommitteeMember,
    NTSCommitteeSection,
    Publication,
    PublicationStats,
    VestnikRelease,
    ScopusMetrics,
    ScopusDocumentType,
    ScopusPublication,
    ScopusStats,
    ScopusSection,
    ScopusAuthor,
    ScopusPublicationAuthor,
    ScopusJournal,
    ScopusPublisher,
    VestnikYear,
    WebOfScienceTimeRange,
    WebOfScienceMetric,
    WebOfScienceCategory,
    WebOfScienceCollaboration,
    WebOfScienceJournalQuartile,
    WebOfScienceAdditionalMetric,
    WebOfScienceSection,
    StudentScientificSocietyInfo,
    StudentScientificSocietyStat,
    StudentScientificSocietyFeature,
    StudentScientificSocietyProject,
    StudentScientificSocietyProjectTag,
    StudentScientificSocietyEvent,
    StudentScientificSocietyJoinStep,
    StudentScientificSocietyLeader,
    StudentScientificSocietyContact,
    ScientificPublication
)

class VestnikReleaseInline(admin.StackedInline):
    model = VestnikRelease
    extra = 1
    fields = ("title_ru", "title_kg", "title_en", "pdf_ru", "pdf_kg", "pdf_en", "description_ru", "description_kg", "description_en")


@admin.register(VestnikYear)
class VestnikYearAdmin(admin.ModelAdmin):
    inlines = [VestnikReleaseInline]

admin.site.register(NTSCommitteeRole)
admin.site.register(NTSResearchDirection)
admin.site.register(NTSCommitteeMember)
admin.site.register(NTSCommitteeSection)
admin.site.register(Publication)
admin.site.register(PublicationStats)
admin.site.register(ScopusMetrics)
admin.site.register(ScopusDocumentType)
admin.site.register(ScopusPublication)
admin.site.register(ScopusStats)
admin.site.register(ScopusJournal)
admin.site.register(ScopusPublisher)
admin.site.register(ScopusSection)
admin.site.register(ScopusAuthor)
admin.site.register(ScopusPublicationAuthor)

# Web of Science
admin.site.register(WebOfScienceTimeRange)
admin.site.register(WebOfScienceMetric)
admin.site.register(WebOfScienceCategory)
admin.site.register(WebOfScienceCollaboration)
admin.site.register(WebOfScienceJournalQuartile)
admin.site.register(WebOfScienceAdditionalMetric)
admin.site.register(WebOfScienceSection)

# Student Scientific Society
admin.site.register(StudentScientificSocietyInfo)
admin.site.register(StudentScientificSocietyStat)
admin.site.register(StudentScientificSocietyFeature)
admin.site.register(StudentScientificSocietyProject)
admin.site.register(StudentScientificSocietyProjectTag)
admin.site.register(StudentScientificSocietyEvent)
admin.site.register(StudentScientificSocietyJoinStep)
admin.site.register(StudentScientificSocietyLeader)
admin.site.register(StudentScientificSocietyContact)
admin.site.register(ScientificPublication)
