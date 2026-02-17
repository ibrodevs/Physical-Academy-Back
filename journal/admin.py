from django.contrib import admin
from .models import (
    JournalSection,
    EditorialOfficeMember,
    EditorialBoardMember,
    JournalArchive,
    LatestIssue,
)



@admin.register(JournalSection)
class JournalSectionAdmin(admin.ModelAdmin):
    list_display  = ("section", "is_active", "updated_at")
    list_filter   = ("is_active",)
    list_editable = ("is_active",)




@admin.register(EditorialOfficeMember)
class EditorialOfficeMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name_ru", "position_ru", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(EditorialBoardMember)
class EditorialBoardMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name_ru", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(JournalArchive)
class JournalArchiveAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "year", "is_active")
    list_editable = ("is_active",)
    ordering = ("-year",)


@admin.register(LatestIssue)
class LatestIssueAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "year", "is_active")
    list_editable = ("is_active",)
    ordering = ("-year",)