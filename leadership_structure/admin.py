from django.contrib import admin
from .models import (
    BoardOfTrustees, AuditCommission, AcademicCouncil,
    AdministrativeDepartment, AdministrativeUnit,
    Leadership, OrganizationStructure, Document, Profsoyuz
)


admin.site.register(BoardOfTrustees)
admin.site.register(Profsoyuz)




admin.site.register(AuditCommission)



@admin.register(AcademicCouncil)
class AcademicCouncilAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'department', 'email', 'is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_kg', 'name_en', 'position', 'department', 'email']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Основная информация (RU)', {
            'fields': ('name', 'position', 'department', 'achievements')
        }),
        ('Киргизский (KG)', {
            'fields': ('name_kg', 'position_kg', 'department_kg', 'achievements_kg'),
            'classes': ('collapse',)
        }),
        ('Английский (EN)', {
            'fields': ('name_en', 'position_en', 'department_en', 'achievements_en'),
            'classes': ('collapse',)
        }),
        ('Контакты и медиа', {
            'fields': ('email', 'phone', 'image')
        }),
        ('Системные поля', {
            'fields': ('is_active', 'order'),
        }),
    )



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


@admin.register(AdministrativeUnit)
class AdministrativeUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'head', 'location', 'staff', 'email', 'is_active', 'order']
    list_filter = ['is_active', 'color', 'created_at']
    search_fields = ['name', 'name_kg', 'name_en', 'head', 'description', 'email']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Основная информация (RU)', {
            'fields': ('name', 'description', 'head', 'location', 'staff', 'responsibilities')
        }),
        ('Киргизский (KG)', {
            'fields': ('name_kg', 'description_kg', 'head_kg', 'location_kg', 'staff_kg', 'responsibilities_kg'),
            'classes': ('collapse',)
        }),
        ('Английский (EN)', {
            'fields': ('name_en', 'description_en', 'head_en', 'location_en', 'staff_en', 'responsibilities_en'),
            'classes': ('collapse',)
        }),
        ('Контакты и оформление', {
            'fields': ('email', 'phone', 'icon', 'color', 'color_class')
        }),
        ('Системные поля', {
            'fields': ('is_active', 'order'),
        }),
    )


# ========== NEW ADMIN INTERFACES FOR MISSING APIS ==========

@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'leadership_type', 'department', 'email', 'is_active', 'order']
    list_filter = ['leadership_type', 'is_active', 'created_at']
    search_fields = ['name', 'name_kg', 'name_en', 'position', 'department', 'email']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Основная информация (RU)', {
            'fields': ('name', 'position', 'leadership_type', 'department', 'bio', 'achievements', 'education')
        }),
        ('Киргизский (KG)', {
            'fields': ('name_kg', 'position_kg', 'department_kg', 'bio_kg', 'achievements_kg', 'education_kg'),
            'classes': ('collapse',)
        }),
        ('Английский (EN)', {
            'fields': ('name_en', 'position_en', 'department_en', 'bio_en', 'achievements_en', 'education_en'),
            'classes': ('collapse',)
        }),
        ('Контакты и медиа', {
            'fields': ('email', 'phone', 'image', 'experience_years', 'icon')
        }),
        ('Системные поля', {
            'fields': ('is_active', 'order'),
        }),
    )


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


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'document_number', 'document_date', 'file_format', 'is_featured', 'is_active', 'order']
    list_filter = ['document_type', 'is_featured', 'is_active', 'document_date', 'created_at']
    search_fields = ['title', 'title_kg', 'title_en', 'description', 'document_number']
    ordering = ['-document_date', 'order', 'title']
    list_editable = ['order', 'is_active', 'is_featured']
    
    fieldsets = (
        ('Основная информация (RU)', {
            'fields': ('title', 'document_type', 'description')
        }),
        ('Киргизский (KG)', {
            'fields': ('title_kg', 'description_kg'),
            'classes': ('collapse',)
        }),
        ('Английский (EN)', {
            'fields': ('title_en', 'description_en'),
            'classes': ('collapse',)
        }),
        ('Документ и метаданные', {
            'fields': ('file', 'document_number', 'document_date', 'file_size', 'file_format', 'icon')
        }),
        ('Системные поля', {
            'fields': ('is_active', 'is_featured', 'order'),
        }),
    )
