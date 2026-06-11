from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import HealthCheckSerializer


class HealthAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: HealthCheckSerializer,
        },
    )
    def get(self, request):
        serializer = HealthCheckSerializer(instance={"status": "ok"})
        return Response(serializer.data, status=status.HTTP_200_OK)
