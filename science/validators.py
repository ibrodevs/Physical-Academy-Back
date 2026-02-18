from django.core.exceptions import ValidationError

def validate_pdf(file):
    """
    Проверяет, что загруженный файл имеет расширение .pdf
    """
    if not file.name.endswith('.pdf'):
        raise ValidationError("Файл должен быть в формате PDF")
