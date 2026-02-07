from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# drf-spectacular imports
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


# Создание schema_view
schema_view = SpectacularAPIView.as_view()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # API endpoints
    path("api/students/", include("students.urls")),
    path("api/leadership-structure/", include("leadership_structure.urls")),
    path("api/admission/", include("admission.urls")),
    path("api/science/", include("science.urls")),
    path("api/academy/", include("main_page.urls")),
    path("api/banner/", include("banner.urls")),
    path("api/news/", include("news.urls")),
    path("api/announcements/", include("announcements.urls")),
    path("api/events/", include("events.urls")),
    path("api/quotes/", include("quotes.urls")),
    path("api/facts/", include("facts.urls")),
    # Sports API
    path("api/sports/", include("sports.urls")),
    # IPChain API
    path("api/ipchain/", include("ipchain_app.urls")),
    # Faculty APIs
    path("api/faculties/coaching/", include("coaching_faculy.urls")),
    path("api/faculties/military/", include("military_faculty.urls")),
    path("api/faculties/correspondence/", include("correspondence_faculty.urls")),
    path("api/faculties/pedagogical/", include("pedagogical_faculty.urls")),
    # General Departments API
    path("api/general-departments/", include("general_departments.urls")),
    # Education API (магистратура, докторантура, колледж)
    path("api/education/", include("education.urls")),

    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger / Redoc UI
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
