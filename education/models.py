from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField


class Master(models.Model):
    info_ru = RichTextUploadingField(verbose_name=_("информация(Русский)"), blank=True, null=True)
    info_kg = RichTextUploadingField(verbose_name=_("информация(кыргызский)"), blank=True, null=True)
    info_en = RichTextUploadingField(verbose_name=_("информация(английском)"), blank=True, null=True)

    study_plan = models.URLField(blank=True, null=True, verbose_name="план обучения")
    disciplines = models.URLField(blank=True, null=True, verbose_name="дисциплины")


    def get_info(self, language="ru"):
        """Получить название на указанном языке"""
        value = getattr(self, f"info_{language}", None)
        return value if value else self.info_ru
    

    class Meta:
        verbose_name = 'Магистратура'
        verbose_name_plural = 'Магистратура'


class MasterStuff(models.Model):
    master = models.ForeignKey(Master, verbose_name='магистр', on_delete=models.CASCADE)

    fio_kg = models.CharField(max_length=255, verbose_name='фио на кыргызском')
    fio_ru = models.CharField(max_length=255, verbose_name='фио на русском')
    fio_en = models.CharField(max_length=255, verbose_name='фио на английском')

    pos_en = models.CharField(max_length=255, verbose_name='должность на английском')
    pos_kg = models.CharField(max_length=255, verbose_name='должность на кыргызском')
    pos_ru = models.CharField(max_length=255, verbose_name='должность на русском')

    def get_fio(self, lang):
        return getattr(self, f'fio_{lang}', self.fio_ru)
    
    def get_pos(self, lang):
        return getattr(self, f'pos_{lang}', self.pos_ru)
    
    class Meta:
        verbose_name = 'сотрудник магистра'
        verbose_name_plural = 'сотрудники магистра'


class Phd(models.Model):
    info_ru = RichTextUploadingField(verbose_name=_("информация(Русский)"), blank=True, null=True)
    info_kg = RichTextUploadingField(verbose_name=_("информация(кыргызский)"), blank=True, null=True)
    info_en = RichTextUploadingField(verbose_name=_("информация(английском)"), blank=True, null=True)

    study_plan = models.URLField(blank=True, null=True, verbose_name="план обучения")
    disciplines = models.URLField(blank=True, null=True, verbose_name="дисциплины")


    def get_info(self, language="ru"):
        """Получить название на указанном языке"""
        value = getattr(self, f"info_{language}", None)
        return value if value else self.info_ru
    

    class Meta:
        verbose_name = 'Доктурантура'
        verbose_name_plural = 'Доктурантура'

    def __str__(self):
        return 'phd info'


class PhdStuff(models.Model):
    Phd = models.ForeignKey(Phd, verbose_name='магистр', on_delete=models.CASCADE)

    fio_kg = models.CharField(max_length=255, verbose_name='фио на кыргызском')
    fio_ru = models.CharField(max_length=255, verbose_name='фио на русском')
    fio_en = models.CharField(max_length=255, verbose_name='фио на английском')

    pos_en = models.CharField(max_length=255, verbose_name='должность на английском')
    pos_kg = models.CharField(max_length=255, verbose_name='должность на кыргызском')
    pos_ru = models.CharField(max_length=255, verbose_name='должность на русском')

    def get_fio(self, lang):
        return getattr(self, f'fio_{lang}', self.fio_ru)
    
    def get_pos(self, lang):
        return getattr(self, f'pos_{lang}', self.pos_ru)
    
    class Meta:
        verbose_name = 'сотрудник доктурантуры'
        verbose_name_plural = 'сотрудники доктурантуры'


class PhdTabCategory(models.Model):
    """Категории/табы (history, about), management, specializations, departments)"""

    # Многоязычные поля для заголовка
    name_ru = models.CharField(max_length=200, verbose_name=_("Заголовок (Русский)"))
    name_kg = models.CharField(max_length=200, verbose_name=_("Заголовок (Кыргызча)"))
    name_en = models.CharField(max_length=200, verbose_name=_("Заголовок (English)"))

    # Цвета для UI (опционально)
    color = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Цвет"),
        help_text="Например: blue-500, green-600",
    )


    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Категория кафедры(доктурантура)")
        verbose_name_plural = _("Категории кафедр(доктурантура)")
        ordering = ["order"]

    def __str__(self):
        return self.name_ru

    def get_name(self, language="ru"):
        """Получить название на указанном языке"""
        value = getattr(self, f"name_{language}", None)
        return value if value else self.name_ru



class PhdDepartmentInfo(models.Model):
    """Описание кафедры"""

    category = models.OneToOneField(
        PhdTabCategory,
        on_delete=models.CASCADE,
        related_name="info",
        verbose_name=_("Категория"),
    )

    # Многоязычные поля для описания
    description_ru = RichTextUploadingField(verbose_name=_("Описание(Русский)"), blank=True, null=True)
    description_kg = RichTextUploadingField(verbose_name=_("Описание(Кыргызча)"), blank=True, null=True)
    description_en = RichTextUploadingField(verbose_name=_("Описание(English)"), blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Описание кафедры (доктурантура)")
        verbose_name_plural = _("Описания кафедр (доктурантура)")

    def __str__(self):
        return f"{self.category.name_ru} - Описание"

    def get_description(self, language="ru"):
        """Получить описание на указанном языке"""
        value = getattr(self, f"description_{language}", None)
        return value if value else self.description_ru

class PhdManagement(models.Model):
    """Руководство факультета (Management)"""

    department = models.ForeignKey(
        PhdTabCategory,
        on_delete=models.CASCADE,
        related_name="management",
        verbose_name=_("Кафедра"),
        blank=True,
        null=True,
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


    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Руководство (доктурантура)")
        verbose_name_plural = _("Руководство (доктурантура)")
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




class CollegeTabCategory(models.Model):
    """Категории/табы (history, about, management, specializations, departments)"""

    # Многоязычные поля для заголовка
    name_ru = models.CharField(max_length=200, verbose_name=_("Заголовок (Русский)"))
    name_kg = models.CharField(max_length=200, verbose_name=_("Заголовок (Кыргызча)"))
    name_en = models.CharField(max_length=200, verbose_name=_("Заголовок (English)"))

    # Цвета для UI (опционально)
    color = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Цвет"),
        help_text="Например: blue-500, green-600",
    )


    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Категория кафедры (колледж)")
        verbose_name_plural = _("Категории кафедр (колледж)")
        ordering = ["order"]

    def __str__(self):
        return self.name_ru

    def get_name(self, language="ru"):
        """Получить название на указанном языке"""
        value = getattr(self, f"name_{language}", None)
        return value if value else self.name_ru



class CollegeDepartmentInfo(models.Model):
    """Описание кафедры"""

    category = models.OneToOneField(
        CollegeTabCategory,
        on_delete=models.CASCADE,
        related_name="info",
        verbose_name=_("Категория"),
    )

    # Многоязычные поля для описания
    description_ru = RichTextUploadingField(verbose_name=_("Описание(Русский)"), blank=True, null=True)
    description_kg = RichTextUploadingField(verbose_name=_("Описание(Кыргызча)"), blank=True, null=True)
    description_en = RichTextUploadingField(verbose_name=_("Описание(English)"), blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Описание кафедры (колледж)")
        verbose_name_plural = _("Описания кафедр (колледж)")

    def __str__(self):
        return f"{self.category.name_ru} - Описание"

    def get_description(self, language="ru"):
        """Получить описание на указанном языке"""
        value = getattr(self, f"description_{language}", None)
        return value if value else self.description_ru


class CollegeManagement(models.Model):
    """Руководство факультета (Management)"""

    department = models.ForeignKey(
        CollegeTabCategory,
        on_delete=models.CASCADE,
        related_name="management",
        verbose_name=_("Кафедра"),
        blank=True,
        null=True,
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


    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Руководство (колледж)")
        verbose_name_plural = _("Руководство (колледж)")
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

