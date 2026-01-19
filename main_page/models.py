from django.db import models
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class aboutStatistics(models.Model):
    titleInt = models.CharField(max_length=200, verbose_name="цифры типа 15+")
    description_ru = models.CharField(
        max_length=500, verbose_name="Описание на русском"
    )
    description_en = models.CharField(
        max_length=500, verbose_name="Описание на английском"
    )
    description_kg = models.CharField(
        max_length=500, verbose_name="Описание на кыргызском"
    )
    emoji = models.CharField(max_length=50, verbose_name="эмодзи")

    class Meta:
        verbose_name = "Статистика на главной"
        verbose_name_plural = "Статистики на главной"

    def __str__(self):
        return self.titleInt

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)


class AboutPhotos(models.Model):
    photo = models.ImageField(
        upload_to="about_photos/", verbose_name="Фото для секции о нас"
    )
    description_ru = models.CharField(
        max_length=500, verbose_name="Описание на русском", blank=True
    )
    description_en = models.CharField(
        max_length=500, verbose_name="Описание на английском", blank=True
    )
    description_kg = models.CharField(
        max_length=500, verbose_name="Описание на кыргызском", blank=True
    )

    class Meta:
        verbose_name = "Фото для секции о нас"
        verbose_name_plural = "Фото для секции о нас"

    def __str__(self):
        return f"Фото {self.id} для секции о нас"

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)


class History(models.Model):
    image = CloudinaryField(
        verbose_name=("Главное изображение")
    )
    text_ru = RichTextUploadingField(null=True, blank=True, verbose_name=("Текст истории(русский)"))
    text_en = RichTextUploadingField(null=True, blank=True, verbose_name=("Текст истории(английский)"))
    text_kg = RichTextUploadingField(null=True, blank=True, verbose_name=("Текст истории(кыргызский)"))

    class Meta:
        verbose_name = "История академии"
        verbose_name_plural = "Истории академии"
    
    def __str__(self):
        return f"История {self.id}"
    
    def get_text(self, language="ru"):
        return getattr(self, f"text_{language}", self.text_ru)
    




class Mission(models.Model):

    title_ru = models.CharField(
        max_length=200, verbose_name="Заголовок миссии(русский)"
    )
    title_en = models.CharField(
        max_length=200, verbose_name="Заголовок миссии(английский)"
    )
    title_kg = models.CharField(
        max_length=200, verbose_name="Заголовок миссии(киргизский)"
    )
    description_ru = RichTextUploadingField(verbose_name="Описание на русском", null=True, blank=True)
    description_en = RichTextUploadingField(verbose_name="Описание на английском", null=True, blank=True)
    description_kg = RichTextUploadingField(verbose_name="Описание на кыргызском", null=True, blank=True)

    pdf_ru = models.FileField(
        upload_to="mission_pdfs/", verbose_name="PDF файл для миссии(русский)", blank=True, null=True
    )
    pdf_en = models.FileField(
        upload_to="mission_pdfs/", verbose_name="PDF файл для миссии(английский)", blank=True, null=True
    )
    pdf_kg = models.FileField(
        upload_to="mission_pdfs/", verbose_name="PDF файл для миссии(кыргызский)", blank=True, null=True
    )

    class Meta:
        verbose_name = "Миссия"
        verbose_name_plural = "Миссии"

    def __str__(self):
        return self.title_ru

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)

    def get_title(self, language="ru"):
        return getattr(self, f"title_{language}", self.title_ru)



class Accreditation(models.Model):
    # Основная информация — три языка для текстов
    name_ru = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    name_kg = models.CharField(max_length=200)

    description_ru = RichTextUploadingField(verbose_name="Описание на русском", null=True, blank=True)
    description_en = RichTextUploadingField(verbose_name="Описание на английском", null=True, blank=True)
    description_kg = RichTextUploadingField(verbose_name="Описание на кыргызском", null=True, blank=True)

    pdf_ru = models.FileField(
        upload_to="accreditation_pdfs/", verbose_name="PDF файл для аккредитации(русский)", blank=True, null=True
    )
    pdf_en = models.FileField(
        upload_to="accreditation_pdfs/", verbose_name="PDF файл для аккредитации(английский)", blank=True, null=True
    )
    pdf_kg = models.FileField(
        upload_to="accreditation_pdfs/", verbose_name="PDF файл для аккредитации(кыргызский)", blank=True, null=True
    )   


    class Meta:
        verbose_name = "Аккредитация"
        verbose_name_plural = "Аккредитации"

    def __str__(self):
        return self.name_ru

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)

    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)

    


class AcademyStatistics(models.Model):
    titleInt = models.CharField(max_length=100, verbose_name="заголовок-цифры типа 15+")
    title_ru = models.CharField(max_length=250, verbose_name="заголовок на русском")
    title_en = models.CharField(max_length=250, verbose_name="заголовок на английском")
    title_kg = models.CharField(max_length=250, verbose_name="заголовок на киргизском")
    description_ru = models.TextField(verbose_name="описание на русском")
    description_en = models.TextField(verbose_name="описание на английском")
    description_kg = models.TextField(verbose_name="описание на киргизском")
    emoji = models.CharField(
        max_length=50,
        verbose_name="эмодзи",
    )

    class Meta:
        verbose_name = "Статистика академии"
        verbose_name_plural = "Статистики академии"

    def get_title(self, language="ru"):
        return getattr(self, f"title_{language}", self.title_ru)

    def get_description(self, language="ru"):
        return getattr(self, f"descripton_{language}", self.description_ru)


class AcademyAchievements(models.Model):
    year = models.PositiveBigIntegerField(verbose_name="год ")
    title_ru = models.CharField(max_length=500, verbose_name="заголовок на русском")
    title_en = models.CharField(max_length=500, verbose_name="заголовок на английском")
    title_kg = models.CharField(max_length=500, verbose_name="заголовок на киргизском")
    description_ru = models.TextField(verbose_name="описание на русском")
    description_en = models.TextField(verbose_name="описание на английском")
    description_kg = models.TextField(verbose_name="описание на киргизском")

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"

    def get_title(self, language="ru"):
        return getattr(self, f"title_{language}", self.title_ru)

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)


class AcademyInfrastructure(models.Model):
    emoji = models.CharField(
        max_length=50,
        verbose_name="эмодзи",
    )
    titleInt = models.CharField(
        max_length=20, verbose_name="заголовок-цифра типа 1000+"
    )

    description_ru = models.CharField(
        max_length=250, verbose_name="описание на русском"
    )
    description_en = models.CharField(
        max_length=250, verbose_name="описание на английском"
    )
    description_kg = models.CharField(
        max_length=250, verbose_name="описание на киргизском"
    )

    class Meta:
        verbose_name = "Инфраструктура"
        verbose_name_plural = "Инфраструктуры"

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)
