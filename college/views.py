from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
import mimetypes
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
from .models import (
    TabCategory,
    Card,
    TimelineEvent,
    AboutCollege,
    Management,
    Teacher,
    Specialization,
    Department,
    DepartmentStaff,
    GalleryCard,
    MissionStrategy,
)
from .serializers import (
    TabCategorySerializer,
    CardSerializer,
    TimelineEventSerializer,
    AboutCollegeSerializer,
    ManagementSerializer,
    TeacherSerializer,
    SpecializationSerializer,
    DepartmentSerializer,
    GalleryCardSerializer,
    MissionStrategySerializer,
)


class GalleryCardListAPIView(generics.ListAPIView):
    """
    API для получения всех карточек галереи колледжа

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)

    Returns:
        [
            {"id": 1, "title": "Заголовок", "description": "Описание", "image": "url", "order": 1},
            ...
        ]
    """

    queryset = GalleryCard.objects.all()
    serializer_class = GalleryCardSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.query_params.get("lang", "ru")
        context.update({"language": language})
        return context


class CollegeAPIRootView(APIView):
    """
    Корневой API эндпоинт колледжа
    Показывает все доступные эндпоинты
    """

    def get(self, request, format=None):
        return Response(
            {
                "tabs": reverse(
                    "college:tabs", request=request, format=format
                ),
                "cards": reverse(
                    "college:cards", request=request, format=format
                ),
                "history": reverse(
                    "college:history", request=request, format=format
                ),
                "about": reverse(
                    "college:about", request=request, format=format
                ),
                "management": reverse(
                    "college:management", request=request, format=format
                ),
                "teachers": reverse(
                    "college:teachers", request=request, format=format
                ),
                "specializations": reverse(
                    "college:specializations",
                    request=request,
                    format=format,
                ),
                "departments": reverse(
                    "college:departments", request=request, format=format
                ),
                "mission_strategy": reverse(
                    "college:mission-strategy", request=request, format=format
                ),
            }
        )


class CollegeTabsAPIView(APIView):
    """
    API для получения всех табов (категорий) колледжа

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)

    Returns:
        [
            {"id": 1, "key": "history", "title": "История", "icon": "📜", "order": 1},
            {"id": 2, "key": "about", "title": "О колледже", "icon": "ℹ️", "order": 2}
        ]
    """

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        tabs = TabCategory.objects.filter(is_active=True).order_by("order")
        serializer = TabCategorySerializer(
            tabs, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeCardsAPIView(APIView):
    """
    API для получения карточек для конкретного таба

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)
        - tab: key таба (например: about, management) - обязательный параметр

    Returns:
        [
            {"id": 1, "title": "Миссия", "description": "Текст...", "order": 1},
            {"id": 2, "title": "Цели", "description": "Текст...", "order": 2}
        ]
    """

    def get(self, request):
        language = request.query_params.get("lang", "ru")
        tab_key = request.query_params.get("tab")

        if not tab_key:
            return Response(
                {"error": "Параметр 'tab' обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tab = TabCategory.objects.get(key=tab_key, is_active=True)
        except TabCategory.DoesNotExist:
            return Response(
                {"error": f"Таб с ключом '{tab_key}' не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cards = Card.objects.filter(tab=tab, is_active=True).order_by("order")
        serializer = CardSerializer(
            cards, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeHistoryAPIView(APIView):
    """
    API для получения событий истории (timeline)

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)

    Returns:
        [
            {"id": 1, "year": "1990", "event": "Основание академии", "order": 1},
            {"id": 2, "year": "2000", "event": "Получение аккредитации", "order": 2}
        ]
    """

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        # Получаем таб с ключом history
        try:
            history_tab = TabCategory.objects.get(key="history", is_active=True)
            timeline = TimelineEvent.objects.filter(
                tab=history_tab, is_active=True
            ).order_by("order")
        except TabCategory.DoesNotExist:
            # Если таб history не найден, возвращаем пустой список
            timeline = TimelineEvent.objects.none()

        serializer = TimelineEventSerializer(
            timeline, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeAboutAPIView(APIView):
    """API для получения текста 'О колледже' (about_college)"""

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        try:
            about_tab = TabCategory.objects.get(key="about_college", is_active=True)
            items = AboutCollege.objects.filter(tab=about_tab, is_active=True).order_by(
                "order"
            )
        except TabCategory.DoesNotExist:
            items = AboutCollege.objects.none()

        serializer = AboutCollegeSerializer(
            items, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeManagementAPIView(APIView):
    """API для получения руководства колледжа (management)

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)
    """

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        try:
            management_tab = TabCategory.objects.get(key="management", is_active=True)
            items = Management.objects.filter(
                tab=management_tab, is_active=True
            ).order_by("order")
        except TabCategory.DoesNotExist:
            items = Management.objects.none()

        serializer = ManagementSerializer(
            items, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeTeachersAPIView(APIView):
    """API для получения преподавателей колледжа (teachers)

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)
    """

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        items = Teacher.objects.filter(is_active=True).order_by("order")
        serializer = TeacherSerializer(
            items, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeSpecializationsAPIView(APIView):
    """API для получения специализаций колледжа (specializations)

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)
    """

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        try:
            spec_tab = TabCategory.objects.get(key="specializations", is_active=True)
            items = Specialization.objects.filter(
                tab=spec_tab, is_active=True
            ).order_by("order")
        except TabCategory.DoesNotExist:
            items = Specialization.objects.none()

        serializer = SpecializationSerializer(
            items, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeDepartmentsAPIView(APIView):
    """API для получения кафедр колледжа с сотрудниками (departments)

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)
    """

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        try:
            dept_tab = TabCategory.objects.get(key="departments", is_active=True)
            items = Department.objects.filter(tab=dept_tab, is_active=True).order_by(
                "order"
            )
        except TabCategory.DoesNotExist:
            items = Department.objects.none()

        serializer = DepartmentSerializer(
            items, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class DownloadResumeView(APIView):
    """
    View для скачивания резюме управления, преподавателей и сотрудников кафедр
    """
    def get(self, request, model_type, pk):
        # Определяем модель по типу
        if model_type == "management":
            obj = get_object_or_404(Management, pk=pk, is_active=True)
        elif model_type == "teacher":
            obj = get_object_or_404(Teacher, pk=pk, is_active=True)
        elif model_type == "staff":
            obj = get_object_or_404(DepartmentStaff, pk=pk, is_active=True)
        else:
            raise Http404("Invalid model type")
        
        # Проверяем наличие резюме
        if not obj.resume:
            raise Http404("Resume not found")
        
        try:
            # Получаем URL файла из Cloudinary
            file_url = obj.resume.url
            
            # Если это Cloudinary URL, генерируем signed URL
            if 'cloudinary.com' in file_url:
                # Извлекаем public_id из URL
                if '/media/' in file_url:
                    # Формат: .../v1/media/path/to/file.pdf или .../media/path/to/file.pdf
                    parts = file_url.split('/media/')
                    if len(parts) > 1:
                        # Убираем version если есть (v1/)
                        public_id_part = parts[1]
                        # Извлекаем public_id (все до последнего расширения)
                        # Для Cloudinary public_id включает путь но без расширения
                        public_id = 'media/' + public_id_part.rsplit('.', 1)[0] if '.' in public_id_part else 'media/' + public_id_part
                        
                        # Генерируем authenticated URL через Cloudinary API
                        signed_url = cloudinary.utils.cloudinary_url(
                            public_id,
                            resource_type="raw",
                            type="upload",
                            sign_url=True,
                            secure=True,
                        )[0]
                        
                        # Скачиваем файл по signed URL
                        response = requests.get(signed_url, timeout=30)
                        response.raise_for_status()
                        file_content = response.content
                else:
                    # Пробуем скачать напрямую
                    response = requests.get(file_url, timeout=30)
                    response.raise_for_status()
                    file_content = response.content
            else:
                # Для не-Cloudinary файлов читаем напрямую
                file = obj.resume.open('rb')
                file_content = file.read()
                file.close()
            
            # Получаем имя файла
            filename = obj.resume.name.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            # Создаем ответ с файлом
            response = HttpResponse(file_content, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            response['Content-Length'] = len(file_content)
            response['Cache-Control'] = 'public, max-age=3600'
            
            return response
        except requests.exceptions.RequestException as e:
            raise Http404(f"Error downloading file from Cloudinary: {str(e)}")
        except Exception as e:
            raise Http404(f"Error reading file: {str(e)}")


class CollegeMissionStrategyAPIView(APIView):
    """API для получения миссий и стратегий колледжа

    Query Parameters:
        - lang: ru, en, kg (по умолчанию: ru)
    """

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        items = MissionStrategy.objects.filter(is_active=True).order_by("order")
        serializer = MissionStrategySerializer(
            items, many=True, context={"request": request, "language": language}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class DownloadMissionStrategyPDFView(APIView):
    """
    View для скачивания PDF файлов миссий и стратегий
    """
    def get(self, request, pk, lang="ru"):
        # Получаем объект миссии/стратегии
        obj = get_object_or_404(MissionStrategy, pk=pk, is_active=True)
        
        # Проверяем язык и получаем соответствующий PDF
        if lang not in ["ru", "kg", "en"]:
            lang = "ru"  # По умолчанию русский
            
        pdf_field = getattr(obj, f"pdf_{lang}", None)
        if not pdf_field:
            # Если нет файла на запрашиваемом языке, используем русский как fallback
            pdf_field = obj.pdf_ru
            
        if not pdf_field:
            raise Http404("PDF file not found")
        
        try:
            # Получаем URL файла
            file_url = pdf_field.url
            
            # Если это Cloudinary URL, генерируем signed URL
            if 'cloudinary.com' in file_url:
                if '/media/' in file_url:
                    parts = file_url.split('/media/')
                    if len(parts) > 1:
                        public_id_part = parts[1]
                        public_id = 'media/' + public_id_part.rsplit('.', 1)[0] if '.' in public_id_part else 'media/' + public_id_part
                        
                        # Генерируем authenticated URL через Cloudinary API
                        signed_url = cloudinary.utils.cloudinary_url(
                            public_id,
                            resource_type="raw",
                            type="upload",
                            sign_url=True,
                            secure=True,
                        )[0]
                        
                        response = requests.get(signed_url, timeout=30)
                        response.raise_for_status()
                        file_content = response.content
                else:
                    response = requests.get(file_url, timeout=30)
                    response.raise_for_status()
                    file_content = response.content
            else:
                # Для не-Cloudinary файлов читаем напрямую
                file = pdf_field.open('rb')
                file_content = file.read()
                file.close()
            
            # Получаем имя файла
            filename = pdf_field.name.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            # Создаем ответ с файлом
            response = HttpResponse(file_content, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            response['Content-Length'] = len(file_content)
            response['Cache-Control'] = 'public, max-age=3600'
            
            return response
        except requests.exceptions.RequestException as e:
            raise Http404(f"Error downloading file from Cloudinary: {str(e)}")
        except Exception as e:
            raise Http404(f"Error reading file: {str(e)}")