from django.contrib import admin
from .models import (
    TabCategory,
    Card,
    TimelineEvent,
    AboutCollege,
    Management,
    Teacher,
    Specialization,
    Department,
    DepartmentStaff,
    GalleryCard,
    MissionStrategy,
)

admin.site.register(GalleryCard)

class CardInline(admin.TabularInline):
    model = Card
    extra = 1
    fields = (
        "title_ru",
        "title_kg",
        "title_en",
        "description_ru",
        "order",
        "is_active",
    )


@admin.register(TabCategory)
class TabCategoryAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "key", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title_ru", "title_kg", "title_en", "key")
    ordering = ("order",)
    fieldsets = (
        (None, {"fields": ("key", "order", "is_active")}),
        ("Заголовки", {"fields": ("title_ru", "title_kg", "title_en")}),
        ("Иконка", {"fields": ("icon",)}),
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "tab", "order", "is_active", "created_at")
    list_filter = ("tab", "is_active", "created_at")
    search_fields = (
        "title_ru",
        "title_kg",
        "title_en",
        "description_ru",
        "description_kg",
        "description_en",
    )
    ordering = ("tab", "order")
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("tab", "order", "is_active")}),
        ("Заголовки", {"fields": ("title_ru", "title_kg", "title_en")}),
        (
            "Описания",
            {"fields": ("description_ru", "description_kg", "description_en")},
        ),
    )


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("tab", "event_preview", "order", "is_active", "created_at")
    list_filter = ("tab", "is_active", "created_at")
    search_fields = ("event_ru", "event_kg", "event_en")
    ordering = ("order",)
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("tab", "image", "order", "is_active")}),
        ("События", {"fields": ("event_ru", "event_kg", "event_en")}),
    )

    def event_preview(self, obj):
        text = obj.event_ru or ""
        return text[:100] + "..." if len(text) > 100 else text

    event_preview.short_description = "Событие"


@admin.register(AboutCollege)
class AboutCollegeAdmin(admin.ModelAdmin):
    list_display = ("tab", "text_preview", "order", "is_active", "created_at")
    list_filter = ("tab", "is_active", "created_at")
    search_fields = ("text_ru", "text_kg", "text_en")
    ordering = ("order",)
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("tab", "order", "is_active")}),
        ("Тексты", {"fields": ("text_ru", "text_kg", "text_en")}),
    )

    def text_preview(self, obj):
        text = obj.text_ru or ""
        return text[:100] + "..." if len(text) > 100 else text

    text_preview.short_description = "Текст"


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ("name_ru", "role_ru", "phone", "email", "order", "is_active")
    list_filter = ("tab", "is_active", "created_at")
    search_fields = (
        "name_ru",
        "name_kg",
        "name_en",
        "role_ru",
        "role_kg",
        "role_en",
        "phone",
        "email",
    )
    ordering = ("order",)
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("tab", "photo", "order", "is_active")}),
        ("Имена", {"fields": ("name_ru", "name_kg", "name_en")}),
        ("Роли", {"fields": ("role_ru", "role_kg", "role_en")}),
        ("Контакты", {"fields": ("phone", "email")}),
        ("Резюме", {"fields": ("resume",)}),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name_ru", "subject_ru", "phone", "email", "order", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = (
        "name_ru",
        "name_kg",
        "name_en",
        "subject_ru",
        "subject_kg",
        "subject_en",
        "phone",
        "email",
    )
    ordering = ("order",)
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("photo", "order", "is_active")}),
        ("Имена", {"fields": ("name_ru", "name_kg", "name_en")}),
        ("Предметы/Специальности", {"fields": ("subject_ru", "subject_kg", "subject_en")}),
        ("Контакты", {"fields": ("phone", "email")}),
        ("Резюме", {"fields": ("resume",)}),
    )


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "order", "is_active", "created_at")
    list_filter = ("tab", "is_active", "created_at")
    search_fields = (
        "title_ru",
        "title_kg",
        "title_en",
        "description_ru",
        "description_kg",
        "description_en",
    )
    ordering = ("order",)
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("tab", "order", "is_active")}),
        ("Названия", {"fields": ("title_ru", "title_kg", "title_en")}),
        (
            "Описания",
            {"fields": ("description_ru", "description_kg", "description_en")},
        ),
    )


class DepartmentStaffInline(admin.TabularInline):
    model = DepartmentStaff
    extra = 1
    fields = (
        "name_ru",
        "name_kg",
        "name_en",
        "position_ru",
        "position_kg",
        "position_en",
        "resume",
        "order",
        "is_active",
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name_ru", "order", "is_active", "created_at")
    list_filter = ("tab", "is_active", "created_at")
    search_fields = (
        "name_ru",
        "name_kg",
        "name_en",
        "description_ru",
        "description_kg",
        "description_en",
    )
    ordering = ("order",)
    list_editable = ("order", "is_active")
    inlines = [DepartmentStaffInline]
    fieldsets = (
        (None, {"fields": ("tab", "order", "is_active")}),
        ("Названия", {"fields": ("name_ru", "name_kg", "name_en")}),
        (
            "Описания",
            {"fields": ("description_ru", "description_kg", "description_en")},
        ),
    )


@admin.register(DepartmentStaff)
class DepartmentStaffAdmin(admin.ModelAdmin):
    list_display = ("name_ru", "position_ru", "department", "order", "is_active")
    list_filter = ("department", "is_active", "created_at")
    search_fields = (
        "name_ru",
        "name_kg",
        "name_en",
        "position_ru",
        "position_kg",
        "position_en",
    )
    ordering = ("department", "order")
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("department", "order", "is_active")}),
        ("Имена", {"fields": ("name_ru", "name_kg", "name_en")}),
        ("Должности", {"fields": ("position_ru", "position_kg", "position_en")}),
        ("Резюме", {"fields": ("resume",)}),
    )


@admin.register(MissionStrategy)
class MissionStrategyAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "order", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title_ru", "title_kg", "title_en")
    ordering = ("order",)
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("order", "is_active")}),
        ("Названия", {"fields": ("title_ru", "title_kg", "title_en")}),
        ("PDF файлы", {"fields": ("pdf_ru", "pdf_kg", "pdf_en")}),
    )