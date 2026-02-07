from django.contrib import admin
from .models import (
    BachelorProgram,
    BachelorFaculties,
    CollegeAdmissionSteps,
    CollegePrograms,
    CollegeStatistics,
    QuotaType,
    QuotaRequirement,
    QuotaBenefit,
    QuotaStats,
    AdditionalSupport,
    ProcessStep,
    AspirantRequirements,
    AspirantMainDate,
    AspirantDocuments,
    AspirantPrograms,
    Master,
    Doctorate,
    CollegeSoonEvents,
    CollegeAdmissionRequirements,
)

class BachelorFacultiesInline(admin.TabularInline):
    model = BachelorFaculties

@admin.register(BachelorProgram)
class BachelorProgramAdmin(admin.ModelAdmin):
    inlines = [BachelorFacultiesInline]

class QuotaRequirementInline(admin.TabularInline):
    """Inline админка для требований к квотам"""

    model = QuotaRequirement
    extra = 1
    fields = (
        "requirement_ru",
        "requirement_kg",
        "requirement_en",
        "order",
        "is_active",
    )


class QuotaBenefitInline(admin.TabularInline):
    """Inline админка для преимуществ квот"""

    model = QuotaBenefit
    extra = 1
    fields = ("benefit_ru", "benefit_kg", "benefit_en", "order", "is_active")


@admin.register(QuotaType)
class QuotaTypeAdmin(admin.ModelAdmin):
    """Админка для типов квот"""

    list_display = [
        "type",
        "title_ru",
        "spots",
        "deadline",
        "color",
        "is_active",
        "order",
    ]
    list_filter = ["color", "is_active", "type"]
    search_fields = ["title_ru", "title_kg", "title_en", "description_ru"]
    list_editable = ["order", "is_active", "spots"]

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "type",
                    "icon",
                    "spots",
                    "deadline",
                    "color",
                    "order",
                    "is_active",
                )
            },
        ),
        ("Название на языках", {"fields": ("title_ru", "title_kg", "title_en")}),
        (
            "Описание на языках",
            {"fields": ("description_ru", "description_kg", "description_en")},
        ),
    )

    inlines = [QuotaRequirementInline, QuotaBenefitInline]


@admin.register(QuotaRequirement)
class QuotaRequirementAdmin(admin.ModelAdmin):
    """Админка для требований к квотам"""

    list_display = ["quota_type", "requirement_ru_short", "order", "is_active"]
    list_filter = ["quota_type", "is_active"]
    search_fields = ["requirement_ru", "requirement_kg", "requirement_en"]
    list_editable = ["order", "is_active"]

    fieldsets = (
        ("Основная информация", {"fields": ("quota_type", "order", "is_active")}),
        (
            "Требования на языках",
            {"fields": ("requirement_ru", "requirement_kg", "requirement_en")},
        ),
    )

    def requirement_ru_short(self, obj):
        """Сокращенное отображение требования"""
        return (
            obj.requirement_ru[:50] + "..."
            if len(obj.requirement_ru) > 50
            else obj.requirement_ru
        )

    requirement_ru_short.short_description = "Требование (рус.)"


@admin.register(QuotaBenefit)
class QuotaBenefitAdmin(admin.ModelAdmin):
    """Админка для преимуществ квот"""

    list_display = ["quota_type", "benefit_ru_short", "order", "is_active"]
    list_filter = ["quota_type", "is_active"]
    search_fields = ["benefit_ru", "benefit_kg", "benefit_en"]
    list_editable = ["order", "is_active"]

    fieldsets = (
        ("Основная информация", {"fields": ("quota_type", "order", "is_active")}),
        (
            "Преимущества на языках",
            {"fields": ("benefit_ru", "benefit_kg", "benefit_en")},
        ),
    )

    def benefit_ru_short(self, obj):
        """Сокращенное отображение преимущества"""
        return (
            obj.benefit_ru[:50] + "..." if len(obj.benefit_ru) > 50 else obj.benefit_ru
        )

    benefit_ru_short.short_description = "Преимущество (рус.)"


@admin.register(QuotaStats)
class QuotaStatsAdmin(admin.ModelAdmin):
    """Админка для статистики квот"""

    list_display = ["stat_type", "number", "label_ru", "order", "is_active"]
    list_filter = ["stat_type", "is_active"]
    search_fields = ["label_ru", "label_kg", "label_en"]
    list_editable = ["order", "is_active", "number"]

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("stat_type", "number", "order", "is_active")},
        ),
        ("Подписи на языках", {"fields": ("label_ru", "label_kg", "label_en")}),
        (
            "Описания на языках",
            {"fields": ("description_ru", "description_kg", "description_en")},
        ),
    )


@admin.register(AdditionalSupport)
class AdditionalSupportAdmin(admin.ModelAdmin):
    """Админка для дополнительной поддержки"""

    list_display = ["support_ru_short", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["support_ru", "support_kg", "support_en"]
    list_editable = ["order", "is_active"]

    fieldsets = (
        ("Основная информация", {"fields": ("order", "is_active")}),
        ("Поддержка на языках", {"fields": ("support_ru", "support_kg", "support_en")}),
    )

    def support_ru_short(self, obj):
        """Сокращенное отображение поддержки"""
        return (
            obj.support_ru[:50] + "..." if len(obj.support_ru) > 50 else obj.support_ru
        )

    support_ru_short.short_description = "Поддержка (рус.)"


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    """Админка для шагов процесса"""

    list_display = ["step_number", "title_ru", "color_scheme", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["title_ru", "title_kg", "title_en", "description_ru"]
    list_editable = ["is_active"]
    ordering = ["step_number"]

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("step_number", "color_scheme", "is_active")},
        ),
        ("Названия на языках", {"fields": ("title_ru", "title_kg", "title_en")}),
        (
            "Описания на языках",
            {"fields": ("description_ru", "description_kg", "description_en")},
        ),
    )


admin.site.register(AspirantRequirements)
admin.site.register(AspirantMainDate)
admin.site.register(AspirantDocuments)
admin.site.register(AspirantPrograms)
admin.site.register(Master)
admin.site.register(Doctorate)
admin.site.register(CollegeSoonEvents)
admin.site.register(CollegeAdmissionSteps)
admin.site.register(CollegeAdmissionRequirements)
admin.site.register(CollegeStatistics)
admin.site.register(CollegePrograms)
