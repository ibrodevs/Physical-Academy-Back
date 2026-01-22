from django.db import models
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField




class TabCategory(models.Model):
    """Категории/табы (history, about, management, specializations, departments)"""

    key = models.CharField(max_length=50, unique=True, verbose_name=_("Ключ"))

    # Многоязычные поля для заголовка
    title_ru = models.CharField(max_length=200, verbose_name=_("Заголовок (Русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Заголовок (Кыргызча)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Заголовок (English)"))

    icon = CloudinaryField(blank=True, null=True, verbose_name=_("Иконка"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    class Meta:
        verbose_name = _("Категория/Таб")
        verbose_name_plural = _("Категории/Табы")
        ordering = ["order"]

    def __str__(self):
        return self.title_ru

    def get_title(self, language="ru"):
        """Получить заголовок на указанном языке"""
        value = getattr(self, f"title_{language}", None)
        return value if value else self.title_ru


class Card(models.Model):
    """Карточки для табов (кроме history)"""

    tab = models.ForeignKey(
        TabCategory,
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name=_("Таб"),
    )

    # Многоязычные поля для заголовка
    title_ru = models.CharField(max_length=200, verbose_name=_("Заголовок (Русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Заголовок (Кыргызча)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Заголовок (English)"))

    # Многоязычные поля для описания
    description_ru = models.TextField(verbose_name=_("Описание (Русский)"))
    description_kg = models.TextField(verbose_name=_("Описание (Кыргызча)"))
    description_en = models.TextField(verbose_name=_("Описание (English)"))

    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Карточка")
        verbose_name_plural = _("Карточки")
        ordering = ["tab", "order"]

    def __str__(self):
        return self.title_ru

    def get_title(self, language="ru"):
        """Получить заголовок на указанном языке"""
        value = getattr(self, f"title_{language}", None)
        return value if value else self.title_ru

    def get_description(self, language="ru"):
        """Получить описание на указанном языке"""
        value = getattr(self, f"description_{language}", None)
        return value if value else self.description_ru


class TimelineEvent(models.Model):
    """События для категории History (timeline)"""

    tab = models.ForeignKey(
        TabCategory,
        on_delete=models.CASCADE,
        related_name="timeline_events",
        verbose_name=_("Таб"),
        limit_choices_to={"key": "history"},
    )
    image = CloudinaryField(blank=True, null=True, verbose_name=_("Картинка"))

    # Многоязычные поля для события
    event_ru = models.TextField(verbose_name=_("Событие (Русский)"))
    event_kg = models.TextField(verbose_name=_("Событие (Кыргызча)"))
    event_en = models.TextField(verbose_name=_("Событие (English)"))

    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Событие истории")
        verbose_name_plural = _("События истории")
        ordering = ["order"]

    def __str__(self):
        return f"{self.event_ru[:50]}"

    def get_event(self, language="ru"):
        """Получить событие на указанном языке"""
        value = getattr(self, f"event_{language}", None)
        return value if value else self.event_ru


class AboutFaculty(models.Model):
    """Описание факультета (About Faculty)"""

    tab = models.ForeignKey(
        TabCategory,
        on_delete=models.CASCADE,
        related_name="about_faculty",
        verbose_name=_("Таб"),
        limit_choices_to={"key": "about_faculty"},
    )

    # Многоязычные поля для текста
    text_ru = RichTextUploadingField(null=True, blank=True)
    text_kg = RichTextUploadingField(null=True, blank=True)
    text_en = RichTextUploadingField(null=True, blank=True)

    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("О факультете")
        verbose_name_plural = _("О факультете")
        ordering = ["order"]

    def __str__(self):
        return f"О факультете - {self.text_ru[:50]}"

    def get_text(self, language="ru"):
        """Получить текст на указанном языке"""
        value = getattr(self, f"text_{language}", None)
        return value if value else self.text_ru


class Management(models.Model):
    """Руководство факультета (Management)"""

    tab = models.ForeignKey(
        TabCategory,
        on_delete=models.CASCADE,
        related_name="management",
        verbose_name=_("Таб"),
        limit_choices_to={"key": "management"},
    )

    photo = CloudinaryField(verbose_name=_("Фото"))

    # Многоязычные поля для имени
    name_ru = models.CharField(max_length=200, verbose_name=_("Имя (Русский)"))
    name_kg = models.CharField(max_length=200, verbose_name=_("Имя (Кыргызча)"))
    name_en = models.CharField(max_length=200, verbose_name=_("Имя (English)"))

    # Многоязычные поля для роли
    role_ru = models.CharField(max_length=200, verbose_name=_("Роль (Русский)"))
    role_kg = models.CharField(max_length=200, verbose_name=_("Роль (Кыргызча)"))
    role_en = models.CharField(max_length=200, verbose_name=_("Роль (English)"))

    phone = models.CharField(
        max_length=50, blank=True, verbose_name=_("Номер телефона")
    )
    email = models.EmailField(blank=True, verbose_name=_("Email"))

    resume = CloudinaryField(
        blank=True,
        null=True,
        resource_type="raw",
        verbose_name=_("Резюме (PDF)"),
    )

    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Руководство")
        verbose_name_plural = _("Руководство")
        ordering = ["order"]

    def __str__(self):
        return f"{self.name_ru} - {self.role_ru}"

    def get_name(self, language="ru"):
        """Получить имя на указанном языке"""
        value = getattr(self, f"name_{language}", None)
        return value if value else self.name_ru

    def get_role(self, language="ru"):
        """Получить роль на указанном языке"""
        value = getattr(self, f"role_{language}", None)
        return value if value else self.role_ru


class Specialization(models.Model):
    """Специализации факультета (Specializations)"""

    tab = models.ForeignKey(
        TabCategory,
        on_delete=models.CASCADE,
        related_name="specializations",
        verbose_name=_("Таб"),
        limit_choices_to={"key": "specializations"},
    )

    # Многоязычные поля для названия специализации
    title_ru = models.CharField(max_length=300, verbose_name=_("Название (Русский)"))
    title_kg = models.CharField(max_length=300, verbose_name=_("Название (Кыргызча)"))
    title_en = models.CharField(max_length=300, verbose_name=_("Название (English)"))

    # Многоязычные поля для описания
    description_ru = models.TextField(blank=True, verbose_name=_("Описание (Русский)"))
    description_kg = models.TextField(blank=True, verbose_name=_("Описание (Кыргызча)"))
    description_en = models.TextField(blank=True, verbose_name=_("Описание (English)"))

    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Специализация")
        verbose_name_plural = _("Специализации")
        ordering = ["order"]

    def __str__(self):
        return self.title_ru

    def get_title(self, language="ru"):
        """Получить название на указанном языке"""
        value = getattr(self, f"title_{language}", None)
        return value if value else self.title_ru

    def get_description(self, language="ru"):
        """Получить описание на указанном языке"""
        value = getattr(self, f"description_{language}", None)
        return value if value else self.description_ru


class Department(models.Model):
    """Кафедры факультета (Departments)"""

    tab = models.ForeignKey(
        TabCategory,
        on_delete=models.CASCADE,
        related_name="departments",
        verbose_name=_("Таб"),
    )

    # Многоязычные поля для названия кафедры
    name_ru = models.CharField(max_length=300, verbose_name=_("Название (Русский)"))
    name_kg = models.CharField(max_length=300, verbose_name=_("Название (Кыргызча)"))
    name_en = models.CharField(max_length=300, verbose_name=_("Название (English)"))

    description_ru = RichTextUploadingField(null=True, blank=True)
    description_kg = RichTextUploadingField(null=True, blank=True)
    description_en = RichTextUploadingField(null=True, blank=True)
    
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Кафедра")
        verbose_name_plural = _("Кафедры")
        ordering = ["order"]

    def __str__(self):
        return self.name_ru

    def get_name(self, language="ru"):
        """Получить название на указанном языке"""
        value = getattr(self, f"name_{language}", None)
        return value if value else self.name_ru

    def get_description(self, language="ru"):
        """Получить описание на указанном языке"""
        value = getattr(self, f"description_{language}", None)
        return value if value else self.description_ru

class DepartmentStaff(models.Model):
    """Сотрудники кафедры (Department Staff)"""

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="staff",
        verbose_name=_("Кафедра"),
    )

    # Многоязычные поля для имени
    name_ru = models.CharField(max_length=200, verbose_name=_("Имя (Русский)"))
    name_kg = models.CharField(max_length=200, verbose_name=_("Имя (Кыргызча)"))
    name_en = models.CharField(max_length=200, verbose_name=_("Имя (English)"))

    # Многоязычные поля для должности
    position_ru = models.CharField(
        max_length=200, verbose_name=_("Должность (Русский)")
    )
    position_kg = models.CharField(
        max_length=200, verbose_name=_("Должность (Кыргызча)")
    )
    position_en = models.CharField(
        max_length=200, verbose_name=_("Должность (English)")
    )

    resume = models.FileField(
        upload_to="pedagogical_faculty/departments/resumes/",
        blank=True,
        null=True,
        verbose_name=_("Резюме (PDF)"),
    )

    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Сотрудник кафедры")
        verbose_name_plural = _("Сотрудники кафедры")
        ordering = ["department", "order"]

    def __str__(self):
        return f"{self.name_ru} - {self.position_ru}"

    def get_name(self, language="ru"):
        """Получить имя на указанном языке"""
        value = getattr(self, f"name_{language}", None)
        return value if value else self.name_ru

    def get_position(self, language="ru"):
        """Получить должность на указанном языке"""
        value = getattr(self, f"position_{language}", None)
        return value if value else self.position_ru



class GalleryCard(models.Model):
    """Галерея факультета (Gallery Cards)"""

    photo = CloudinaryField(verbose_name=_("Фото"))
    
    title_ru = models.CharField(max_length=200, blank=True, verbose_name=_("Заголовок (Русский)"))
    title_kg = models.CharField(max_length=200, blank=True, verbose_name=_("Заголовок (Кыргызча)"))
    title_en = models.CharField(max_length=200, blank=True, verbose_name=_("Заголовок (English)"))  

    description_ru = models.TextField(blank=True, verbose_name=_("Описание (Русский)"))
    description_kg = models.TextField(blank=True, verbose_name=_("Описание (Кыргызча)"))
    description_en = models.TextField(blank=True, verbose_name=_("Описание (English)")) 


    class Meta:
        verbose_name = _("Карточка галереи")
        verbose_name_plural = _("Карточки галереи")
        ordering = ["id"] 

    def __str__(self):
        return f"Галерея - {self.title_ru[:50]}"
    def get_title(self, language="ru"):
        """Получить заголовок на указанном языке"""
        value = getattr(self, f"title_{language}", None)
        return value if value else self.title_ru
    def get_description(self, language="ru"):
        """Получить описание на указанном языке"""
        value = getattr(self, f"description_{language}", None)
        return value if value else self.description_ru
