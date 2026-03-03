from django.contrib import admin
from .models import (
    JournalSection,
    EditorialBoard,
    LatestIssue,
    ArchiveYear,    ArchiveItem,
)


@admin.register(JournalSection)
class JournalSectionAdmin(admin.ModelAdmin):
    list_display  = ("section", "is_active", "updated_at")
    list_filter   = ("is_active",)
    list_editable = ("is_active",)


@admin.register(EditorialBoard)
class EditorialBoardAdmin(admin.ModelAdmin):
    list_display  = ("title_ru", "is_active", "updated_at")
    list_editable = ("is_active",)


class ArchiveDocumentInline(admin.TabularInline):
    model  = ArchiveItem
    extra  = 1
    fields = ("title_ru", "title_en", "title_kg", "file_ru", "file_en", "file_kg", "sort_order", "is_active")

@admin.register(ArchiveYear)
class ArchiveYearAdmin(admin.ModelAdmin):
    list_display  = ("year", "is_active")
    list_editable = ("is_active",)
    inlines       = [ArchiveDocumentInline]


@admin.register(LatestIssue)
class LatestIssueAdmin(admin.ModelAdmin):
    list_display  = ("title_ru", "year", "is_active")
    list_editable = ("is_active",)
    ordering      = ("-year",)