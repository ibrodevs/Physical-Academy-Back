from django.contrib import admin
from .models import AdministrativeStructure


@admin.register(AdministrativeStructure)
class AdministrativeStructureAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title_ru", "title_en", "title_kg")
    fieldsets = (
        ("Названия", {
            "fields": ("title_ru", "title_en", "title_kg")
        }),
        ("PDF файлы", {
            "fields": ("file_ru", "file_en", "file_kg")
        }),
        ("Настройки", {
            "fields": ("is_active",)
        }),
    )