from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AdministrativeStructure
from .serializers import AdministrativeStructureSerializer

ALLOWED_LANGS = ["ru", "en", "kg"]


class AdministrativeStructureView(APIView):

    def get(self, request):
        lang = request.query_params.get("lang", "ru")

        if lang not in ALLOWED_LANGS:
            return Response(
                {"detail": "Invalid language parameter. Use: ru, en or kg"},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance = AdministrativeStructure.objects.filter(is_active=True).first()

        if not instance:
            return Response(
                {"detail": "Administrative structure not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AdministrativeStructureSerializer(
            instance, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)