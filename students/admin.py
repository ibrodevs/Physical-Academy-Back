from django.contrib import admin
from .models import (
    StudentSupport,
    StudentsCouncil,
    StudentExchange,
    StudentInstractions,
    ScholarshipProgram,
    ScholarshipRequiredDocument,
)

@admin.register(StudentSupport)
class StudentSupportAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(StudentsCouncil)
class StudentsCounseilAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(StudentExchange)
class StudentExchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru')


@admin.register(StudentInstractions)
class StudentInstractionsAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(ScholarshipProgram)
class ScholarshipProgramAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'amount', 'currency', 'application_deadline', 'is_active')
    list_filter = ('is_active', 'currency', 'created_at')
    search_fields = ('name_ru', 'name_en', 'name_kg')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name_ru', 'name_en', 'name_kg')
        }),
        ('Описание и критерии', {
            'fields': ('description_ru', 'description_en', 'description_kg',
                      'eligibility_criteria_ru', 'eligibility_criteria_en', 'eligibility_criteria_kg')
        }),
        ('Финансовые данные', {
            'fields': ('amount', 'currency')
        }),
        ('Контактная информация', {
            'fields': ('contact_email', 'contact_phone', 'application_link', 'application_deadline')
        }),
        ('Статус', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(ScholarshipRequiredDocument)
class ScholarshipRequiredDocumentAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'scholarship', 'is_required', 'order')
    list_filter = ('scholarship', 'is_required')
    search_fields = ('name_ru', 'name_en', 'name_kg')
    ordering = ('scholarship', 'order')
    fieldsets = (
        ('Программа стипендии', {
            'fields': ('scholarship',)
        }),
        ('Название документа', {
            'fields': ('name_ru', 'name_en', 'name_kg')
        }),
        ('Описание документа', {
            'fields': ('description_ru', 'description_en', 'description_kg')
        }),
        ('Параметры', {
            'fields': ('is_required', 'order')
        }),
    )
