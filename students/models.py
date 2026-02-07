from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class StudentSupport(models.Model):
    text_ru = RichTextUploadingField(verbose_name='текст на русском')
    text_en = RichTextUploadingField(verbose_name='текст на английском')
    text_kg = RichTextUploadingField(verbose_name='текст на кыргызском')

    class Meta:
        verbose_name = 'поддержка студентов'

    def get_text(self, lang):
        return getattr(self,f'text_{lang}')
    

class StudentsCouncil(models.Model):    
    text_ru = RichTextUploadingField(verbose_name='текст на русском')
    text_en = RichTextUploadingField(verbose_name='текст на английском')
    text_kg = RichTextUploadingField(verbose_name='текст на кыргызском')

    class Meta:
        verbose_name = 'студентеческий совет'

    def get_text(self, lang):
        return getattr(self,f'text_{lang}')
    

class StudentExchange(models.Model):
    photo = models.ImageField(verbose_name='фото')

    name_ru = models.CharField(max_length=255, verbose_name='название программы на русском')
    name_en = models.CharField(max_length=255, verbose_name='название программы на английском')
    name_kg = models.CharField(max_length=255, verbose_name='название программы на кыргызском')

    desc_ru = models.CharField(max_length=1005, verbose_name='описание программы на русском')
    desc_en = models.CharField(max_length=1005, verbose_name='описание программы на английском')
    desc_kg = models.CharField(max_length=1005, verbose_name='описание программы на кыргызском')

    class Meta:
        verbose_name = 'студентеческий обмен'

    def get_name(self, lang):
        return getattr(self,f'name_{lang}')
    
    def get_desc(self, lang):
        return getattr(self,f'desc_{lang}')


class StudentInstractions(models.Model):
    pdf_ru = models.FileField(verbose_name='pdf(ru)')
    pdf_en = models.FileField(verbose_name='pdf(en)')
    pdf_kg = models.FileField(verbose_name='pdf(kg)')
    

    class Meta:
        verbose_name= 'инструкции'

    def get_pdf(self, lang):
        return getattr(self, f'pdf_{lang}', self.pdf_ru)

class ScholarshipProgram(models.Model):
    """Стипендиальная программа для студентов"""

    name_ru = models.CharField(max_length=200, verbose_name="Название программы (RU)")
    name_en = models.CharField(max_length=200, verbose_name="Название программы (EN)")
    name_kg = models.CharField(max_length=200, verbose_name="Название программы (KG)")

    description_ru = models.TextField(verbose_name="Описание программы (RU)")
    description_en = models.TextField(verbose_name="Описание программы (EN)")
    description_kg = models.TextField(verbose_name="Описание программы (KG)")

    eligibility_criteria_ru = models.TextField(verbose_name="Критерии отбора (RU)")
    eligibility_criteria_en = models.TextField(verbose_name="Критерии отбора (EN)")
    eligibility_criteria_kg = models.TextField(verbose_name="Критерии отбора (KG)")

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма стипендии"
    )
    currency = models.CharField(max_length=10, default="KGS", verbose_name="Валюта")

    application_deadline = models.DateField(verbose_name="Дедлайн подачи заявок")
    application_link = models.URLField(
        blank=True, null=True, verbose_name="Ссылка для подачи заявки"
    )

    contact_email = models.EmailField(
        blank=True, null=True, verbose_name="Контактный email"
    )
    contact_phone = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Контактный телефон"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Scholarship Program"
        verbose_name_plural = "Scholarship Programs"
        ordering = ["name_ru"]

    def __str__(self):
        return self.name_ru

    def get_field(self, field_name, language="ru"):
        """Получить значение поля на указанном языке"""
        field_with_lang = f"{field_name}_{language}"
        return getattr(self, field_with_lang, getattr(self, f"{field_name}_ru"))


class ScholarshipRequiredDocument(models.Model):
    """Документы, необходимые для подачи заявки на стипендию"""

    scholarship = models.ForeignKey(
        ScholarshipProgram,
        on_delete=models.CASCADE,
        related_name="required_documents",
        verbose_name="Стипендиальная программа",
    )

    name_ru = models.CharField(max_length=200, verbose_name="Название документа (RU)")
    name_en = models.CharField(max_length=200, verbose_name="Название документа (EN)")
    name_kg = models.CharField(max_length=200, verbose_name="Название документа (KG)")

    description_ru = models.TextField(
        verbose_name="Описание документа (RU)", blank=True, null=True
    )
    description_en = models.TextField(
        verbose_name="Описание документа (EN)", blank=True, null=True
    )
    description_kg = models.TextField(
        verbose_name="Описание документа (KG)", blank=True, null=True
    )

    is_required = models.BooleanField(default=True, verbose_name="Обязательный")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Порядок")

    class Meta:
        verbose_name = "Required Document"
        verbose_name_plural = "Required Documents"
        ordering = ["scholarship", "order"]

    def __str__(self):
        return f"{self.scholarship.name_ru} - {self.name_ru}"

    def get_field(self, field_name, language="ru"):
        """Получить значение поля на указанном языке"""
        field_with_lang = f"{field_name}_{language}"
        return getattr(self, field_with_lang, getattr(self, f"{field_name}_ru"))
