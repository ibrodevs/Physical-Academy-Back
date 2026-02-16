from django.urls import path
from .views import AdministrativeStructureView

urlpatterns = [
    path("", AdministrativeStructureView.as_view(), name="administrative-structure"),
]