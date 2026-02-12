from django.contrib import admin
from .models import Graduate


@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name_ru", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["full_name_ru", "full_name_en", "full_name_kg"]
    list_editable = ["is_active"]

   
    fieldsets = (
        ("Русский", {
            "fields": ("full_name_ru", "description_ru"),
        }),
        ("English", {
            "fields": ("full_name_en", "description_en"),
        }),
        ("Кыргызча", {
            "fields": ("full_name_kg", "description_kg"),
        }),
        ("Прочее", {
            "fields": ("is_active",),
        }),
    )
