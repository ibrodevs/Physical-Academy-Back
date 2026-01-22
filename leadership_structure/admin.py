from django.contrib import admin
from .models import (
    BoardOfTrustees, AuditCommission, AcademicCouncil,
    AdministrativeDepartment, AdministrativeUnit,
    Leadership, OrganizationStructure, Document, Profsoyuz, Commission
)


admin.site.register(BoardOfTrustees)
admin.site.register(Profsoyuz)

admin.site.register(AcademicCouncil)
admin.site.register(Commission)


admin.site.register(AuditCommission)



@admin.register(AdministrativeDepartment)
class AdministrativeDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head', 'email', 'phone', 'is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_kg', 'name_en', 'head', 'email']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Основная информация (RU)', {
            'fields': ('name', 'head', 'responsibilities')
        }),
        ('Киргизский (KG)', {
            'fields': ('name_kg', 'head_kg', 'responsibilities_kg'),
            'classes': ('collapse',)
        }),
        ('Английский (EN)', {
            'fields': ('name_en', 'head_en', 'responsibilities_en'),
            'classes': ('collapse',)
        }),
        ('Контакты и оформление', {
            'fields': ('email', 'phone', 'icon')
        }),
        ('Системные поля', {
            'fields': ('is_active', 'order'),
        }),
    )

admin.site.register(AdministrativeUnit)

# ========== NEW ADMIN INTERFACES FOR MISSING APIS ==========

@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    pass


@admin.register(OrganizationStructure)
class OrganizationStructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'structure_type', 'head', 'parent', 'staff_count', 'is_active', 'order']
    list_filter = ['structure_type', 'is_active', 'created_at']
    search_fields = ['name', 'name_kg', 'name_en', 'head', 'description']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Основная информация (RU)', {
            'fields': ('name', 'structure_type', 'description', 'head', 'parent', 'responsibilities')
        }),
        ('Киргизский (KG)', {
            'fields': ('name_kg', 'description_kg', 'head_kg', 'responsibilities_kg'),
            'classes': ('collapse',)
        }),
        ('Английский (EN)', {
            'fields': ('name_en', 'description_en', 'head_en', 'responsibilities_en'),
            'classes': ('collapse',)
        }),
        ('Контакты и расположение', {
            'fields': ('email', 'phone', 'location', 'location_kg', 'location_en', 'staff_count', 'icon')
        }),
        ('Системные поля', {
            'fields': ('is_active', 'order'),
        }),
    )

admin.site.register(Document)