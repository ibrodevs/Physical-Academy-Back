from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField


class BoardOfTrustees(models.Model):
    """Попечительский совет / Board of Trustees"""
    
    # Name fields
    name = models.CharField(max_length=200, verbose_name="ФИО (RU)")
    name_kg = models.CharField(max_length=200, verbose_name="ФИО (KG)", blank=True)
    name_en = models.CharField(max_length=200, verbose_name="ФИО (EN)", blank=True)
    
    # Position fields
    position = models.CharField(max_length=200, verbose_name="Должность (RU)")
    position_kg = models.CharField(max_length=200, verbose_name="Должность (KG)", blank=True)
    position_en = models.CharField(max_length=200, verbose_name="Должность (EN)", blank=True)
    
    
    image = CloudinaryField(verbose_name="Фото", blank=True, null=True)
    
    class Meta:
        verbose_name = "Член попечительского совета"
        verbose_name_plural = "Попечительский совет"
    
    def __str__(self):
        return f"{self.name} - {self.position}"

    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)

    def get_position(self, language="ru"):
        return getattr(self, f"position_{language}", self.position_ru)


class AuditCommission(models.Model):
    """Ревизионная комиссия / Audit Commission"""
    text_ru = models.CharField(max_length=200, verbose_name="Текст (RU)")
    text_kg = models.CharField(max_length=200, verbose_name="Текст (KG)")
    text_en = models.CharField(max_length=200, verbose_name="Текст (EN)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    
    class Meta:
        verbose_name = "Член  комиссии"
        verbose_name_plural = " комиссия"
        ordering = ["order", "id"]
    
    def __str__(self):
        return self.text_ru

    def get_text(self, language="ru"):
        return getattr(self, f"text_{language}", self.text_ru)


class AcademicCouncil(models.Model):
    """Ученый совет / Academic Council"""
    
    # Name fields
    name = models.CharField(max_length=200, verbose_name="ФИО (RU)")
    name_kg = models.CharField(max_length=200, verbose_name="ФИО (KG)", blank=True)
    name_en = models.CharField(max_length=200, verbose_name="ФИО (EN)", blank=True)
    
    # Position fields
    position = models.CharField(max_length=200, verbose_name="Должность (RU)")
    position_kg = models.CharField(max_length=200, verbose_name="Должность (KG)", blank=True)
    position_en = models.CharField(max_length=200, verbose_name="Должность (EN)", blank=True)
    
    # Department fields
    department = models.CharField(max_length=200, verbose_name="Кафедра/Отдел (RU)", blank=True)
    department_kg = models.CharField(max_length=200, verbose_name="Кафедра/Отдел (KG)", blank=True)
    department_en = models.CharField(max_length=200, verbose_name="Кафедра/Отдел (EN)", blank=True)
    
    # Achievements (JSON field for list of achievements)
    achievements = models.JSONField(default=list, verbose_name="Достижения (RU)", blank=True)
    achievements_kg = models.JSONField(default=list, verbose_name="Достижения (KG)", blank=True)
    achievements_en = models.JSONField(default=list, verbose_name="Достижения (EN)", blank=True)
    
    # Contact information
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    
    # Image
    image = models.ImageField(upload_to='academic_council/', verbose_name="Фото", blank=True, null=True)
    
    # System fields
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Член ученого совета"
        verbose_name_plural = "Ученый совет"
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class Profsoyuz(models.Model):
    description_ru = RichTextUploadingField(verbose_name="Описание (RU)")
    description_kg = RichTextUploadingField(verbose_name="Описание (KG)", blank=True)
    description_en = RichTextUploadingField(verbose_name="Описание (EN)", blank=True)

    class Meta:
        verbose_name = "Профсоюз"
        verbose_name_plural = "Профсоюз"
    
    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)


class AdministrativeDepartment(models.Model):
    """Административные отделы / Administrative Departments"""
    
    # Name fields
    name = models.CharField(max_length=200, verbose_name="Название (RU)")
    name_kg = models.CharField(max_length=200, verbose_name="Название (KG)", blank=True)
    name_en = models.CharField(max_length=200, verbose_name="Название (EN)", blank=True)
    
    # Head fields
    head = models.CharField(max_length=200, verbose_name="Руководитель (RU)")
    head_kg = models.CharField(max_length=200, verbose_name="Руководитель (KG)", blank=True)
    head_en = models.CharField(max_length=200, verbose_name="Руководитель (EN)", blank=True)
    
    # Responsibilities (JSON field for list)
    responsibilities = models.JSONField(default=list, verbose_name="Обязанности (RU)", blank=True)
    responsibilities_kg = models.JSONField(default=list, verbose_name="Обязанности (KG)", blank=True)
    responsibilities_en = models.JSONField(default=list, verbose_name="Обязанности (EN)", blank=True)
    
    # Contact information
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    
    # Icon
    icon = models.CharField(max_length=50, verbose_name="Иконка", default='🏛️', blank=True)
    
    # System fields
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Административный отдел"
        verbose_name_plural = "Административные отделы"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class AdministrativeUnit(models.Model):
    """Административные подразделения / Administrative Units"""
    
    # Name fields
    name = models.CharField(max_length=200, verbose_name="Название (RU)")
    name_kg = models.CharField(max_length=200, verbose_name="Название (KG)", blank=True)
    name_en = models.CharField(max_length=200, verbose_name="Название (EN)", blank=True)
    
    # Description fields
    description = models.TextField(verbose_name="Описание (RU)")
    description_kg = models.TextField(verbose_name="Описание (KG)", blank=True)
    description_en = models.TextField(verbose_name="Описание (EN)", blank=True)
    
    # Head fields
    head = models.CharField(max_length=200, verbose_name="Руководитель (RU)")
    head_kg = models.CharField(max_length=200, verbose_name="Руководитель (KG)", blank=True)
    head_en = models.CharField(max_length=200, verbose_name="Руководитель (EN)", blank=True)
    
    # Location fields
    location = models.CharField(max_length=200, verbose_name="Местоположение (RU)", blank=True)
    location_kg = models.CharField(max_length=200, verbose_name="Местоположение (KG)", blank=True)
    location_en = models.CharField(max_length=200, verbose_name="Местоположение (EN)", blank=True)
    
    # Staff fields
    staff = models.CharField(max_length=100, verbose_name="Персонал (RU)", blank=True)
    staff_kg = models.CharField(max_length=100, verbose_name="Персонал (KG)", blank=True)
    staff_en = models.CharField(max_length=100, verbose_name="Персонал (EN)", blank=True)
    
    # Responsibilities (JSON field for list)
    responsibilities = models.JSONField(default=list, verbose_name="Обязанности (RU)", blank=True)
    responsibilities_kg = models.JSONField(default=list, verbose_name="Обязанности (KG)", blank=True)
    responsibilities_en = models.JSONField(default=list, verbose_name="Обязанности (EN)", blank=True)
    
    # Contact information
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    
    # Icon
    icon = models.CharField(max_length=50, verbose_name="Иконка", default='🏢', blank=True)
    
    # Color (for UI)
    color = models.CharField(max_length=50, verbose_name="Цвет", default='blue', blank=True)
    color_class = models.CharField(max_length=100, verbose_name="CSS класс цвета", default='from-blue-500 to-blue-600', blank=True)
    
    # System fields
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Административное подразделение"
        verbose_name_plural = "Административные подразделения"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class BoardOfTrusteesStats(models.Model):
    """Статистика попечительского совета / Board of Trustees Statistics"""
    
    # Label fields
    label = models.CharField(max_length=200, verbose_name="Название (RU)")
    label_kg = models.CharField(max_length=200, verbose_name="Название (KG)", blank=True)
    label_en = models.CharField(max_length=200, verbose_name="Название (EN)", blank=True)
    
    # Target value (for counter animation)
    target_value = models.IntegerField(verbose_name="Целевое значение", validators=[MinValueValidator(0)])
    
    # Icon
    icon = models.CharField(max_length=50, verbose_name="Иконка", default='📊', blank=True)
    
    # Color gradient
    color_from = models.CharField(max_length=50, verbose_name="Цвет от", default='blue-500')
    color_to = models.CharField(max_length=50, verbose_name="Цвет до", default='blue-600')
    
    # System fields
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Статистика попечительского совета"
        verbose_name_plural = "Статистика попечительского совета"
        ordering = ['order', 'label']
    
    def __str__(self):
        return f"{self.label}: {self.target_value}"


class AuditCommissionStatistics(models.Model):
    """Статистика ревизионной комиссии / Audit Commission Statistics"""
    
    # Label fields
    label = models.CharField(max_length=200, verbose_name="Название (RU)")
    label_kg = models.CharField(max_length=200, verbose_name="Название (KG)", blank=True)
    label_en = models.CharField(max_length=200, verbose_name="Название (EN)", blank=True)
    
    # Value
    value = models.CharField(max_length=100, verbose_name="Значение (RU)")
    value_kg = models.CharField(max_length=100, verbose_name="Значение (KG)", blank=True)
    value_en = models.CharField(max_length=100, verbose_name="Значение (EN)", blank=True)
    
    # Icon
    icon = models.CharField(max_length=50, verbose_name="Иконка", default='📊', blank=True)
    
    # System fields
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Статистика ревизионной комиссии"
        verbose_name_plural = "Статистика ревизионной комиссии"
        ordering = ['order', 'label']
    
    def __str__(self):
        return f"{self.label}: {self.value}"


# ========== NEW MODELS FOR MISSING APIs ==========

class Leadership(models.Model):
    """Руководство академии / Academy Leadership (для /leadership/)"""
    
    photo = CloudinaryField(verbose_name="Фото", blank=True, null=True)

    position_ru = models.CharField(max_length=200, verbose_name="Должность (RU)", blank=True, null=True)
    position_kg = models.CharField(max_length=200, verbose_name="Должность (KG)", blank=True, null=True)
    position_en = models.CharField(max_length=200, verbose_name="Должность (EN)", blank=True, null=True)
    
    # Name fields
    name_ru = models.CharField(max_length=200, verbose_name="ФИО (RU)", blank=True, null=True)
    name_kg = models.CharField(max_length=200, verbose_name="ФИО (KG)", blank=True, null=True)
    name_en = models.CharField(max_length=200, verbose_name="ФИО (EN)", blank=True, null=True)

    bio_kg = RichTextUploadingField(verbose_name="Биография (KG)", blank=True, null=True)
    bio_en = RichTextUploadingField(verbose_name="Биография (EN)", blank=True, null=True)
    bio_ru = RichTextUploadingField(verbose_name="Биография (RU)" , blank=True, null=True)

    order = models.IntegerField(default=0, verbose_name="Порядок отображения", null=True, blank=True)
    
    class Meta:
        verbose_name = "Ректорат академии"
        verbose_name_plural = "Ректорат академии"

    def __str__(self):
        return self.name_ru
    
    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)

    def get_position(self, language="ru"):
        return getattr(self, f"position_{language}", self.position_ru)
    
    def get_bio(self, language="ru"):
        return getattr(self, f"bio_{language}", self.bio_ru)
    

class OrganizationStructure(models.Model):
    """Организационная структура / Organization Structure (для /organization-structure/)"""
    
    STRUCTURE_TYPE_CHOICES = [
        ('faculty', 'Факультет'),
        ('department', 'Кафедра'),
        ('unit', 'Подразделение'),
        ('service', 'Служба'),
        ('center', 'Центр'),
    ]
    
    # Name fields
    name = models.CharField(max_length=200, verbose_name="Название (RU)")
    name_kg = models.CharField(max_length=200, verbose_name="Название (KG)", blank=True)
    name_en = models.CharField(max_length=200, verbose_name="Название (EN)", blank=True)
    
    # Structure type
    structure_type = models.CharField(
        max_length=50,
        choices=STRUCTURE_TYPE_CHOICES,
        verbose_name="Тип структуры",
        default='department'
    )
    
    # Description
    description = models.TextField(verbose_name="Описание (RU)", blank=True)
    description_kg = models.TextField(verbose_name="Описание (KG)", blank=True)
    description_en = models.TextField(verbose_name="Описание (EN)", blank=True)
    
    # Head
    head = models.CharField(max_length=200, verbose_name="Руководитель (RU)", blank=True)
    head_kg = models.CharField(max_length=200, verbose_name="Руководитель (KG)", blank=True)
    head_en = models.CharField(max_length=200, verbose_name="Руководитель (EN)", blank=True)
    
    # Parent (for hierarchical structure)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Родительская структура"
    )
    
    # Responsibilities
    responsibilities = models.JSONField(default=list, verbose_name="Обязанности (RU)", blank=True)
    responsibilities_kg = models.JSONField(default=list, verbose_name="Обязанности (KG)", blank=True)
    responsibilities_en = models.JSONField(default=list, verbose_name="Обязанности (EN)", blank=True)
    
    # Contact info
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    location = models.CharField(max_length=200, verbose_name="Расположение (RU)", blank=True)
    location_kg = models.CharField(max_length=200, verbose_name="Расположение (KG)", blank=True)
    location_en = models.CharField(max_length=200, verbose_name="Расположение (EN)", blank=True)
    
    # Staff count
    staff_count = models.PositiveIntegerField(default=0, verbose_name="Количество сотрудников")
    
    # Icon
    icon = models.CharField(max_length=50, verbose_name="Иконка", default='🏛️', blank=True)
    
    # System fields
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Организационная структура"
        verbose_name_plural = "Организационная структура"
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_structure_type_display()})"


class Document(models.Model):
    """Документы / Documents (для /documents/)"""
    
    DOCUMENT_TYPE_CHOICES = [
        ('regulation', 'Положение'),
        ('order', 'Приказ'),
        ('instruction', 'Инструкция'),
        ('charter', 'Устав'),
        ('plan', 'План'),
        ('report', 'Отчет'),
        ('other', 'Другое'),
    ]
    
    # Title fields
    title = models.CharField(max_length=200, verbose_name="Название (RU)")
    title_kg = models.CharField(max_length=200, verbose_name="Название (KG)", blank=True)
    title_en = models.CharField(max_length=200, verbose_name="Название (EN)", blank=True)
    
    # Document type
    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name="Тип документа",
        default='other'
    )
    
    # Description
    description = models.TextField(verbose_name="Описание (RU)", blank=True)
    description_kg = models.TextField(verbose_name="Описание (KG)", blank=True)
    description_en = models.TextField(verbose_name="Описание (EN)", blank=True)
    
    # File
    file = models.FileField(upload_to='documents/', verbose_name="Файл", blank=True, null=True)
    
    # Document number/code
    document_number = models.CharField(max_length=100, verbose_name="Номер документа", blank=True)
    
    # Date
    document_date = models.DateField(verbose_name="Дата документа", blank=True, null=True)
    
    # File size and format
    file_size = models.PositiveIntegerField(default=0, verbose_name="Размер файла (байт)")
    file_format = models.CharField(max_length=10, verbose_name="Формат файла", blank=True)
    
    # Icon
    icon = models.CharField(max_length=50, verbose_name="Иконка", default='📄', blank=True)
    
    # System fields
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-document_date', 'order', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.document_number})"
