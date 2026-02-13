from django.contrib import admin
from .models import BulletinYear, BulletinIssue


class BulletinIssueInline(admin.StackedInline):
    """Позволяет добавлять выпуски прямо на странице года."""
    model = BulletinIssue
    extra = 1  # одна пустая форма для нового выпуска
    fields = ['issue_number', 'description_ru', 'description_en', 'description_kg']


@admin.register(BulletinYear)
class BulletinYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'issue_count']
    inlines = [BulletinIssueInline]  # выпуски редактируются внутри года

    def issue_count(self, obj):
        return obj.issues.count()
    issue_count.short_description = "Выпусков"


@admin.register(BulletinIssue)
class BulletinIssueAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'year', 'issue_number', 'created_at']
    list_filter = ['year']
    ordering = ['-year', 'issue_number']