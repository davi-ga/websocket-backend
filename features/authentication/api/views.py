from rest_framework import views, response, status
from drf_spectacular.utils import extend_schema
from django.contrib.auth import login, logout

from features.authentication.api.serializers import AuthenticateSerializer

from core.utils.schemas import SuccessResponseSchema


class AuthenticateAPIView(views.APIView):

    authentication_classes = []
    permission_classes = []
    serializer_class = AuthenticateSerializer

    @extend_schema(responses={"200": SuccessResponseSchema})
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        login(request, user)

        return response.Response({"success": "User has been logged in successfuly"}, status=status.HTTP_200_OK)


class LogoutAPIView(views.APIView):

    permission_classes = []
    authentication_classes = []
    serializer_class = AuthenticateSerializer

    @extend_schema(
        responses={"200": SuccessResponseSchema},
    )
    def post(self, request):

        logout(request)

        return response.Response(
            {"success": "You have been successfully logged out."},
            status=status.HTTP_200_OK,
        )
