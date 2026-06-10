from rest_framework import views, response, status

from features.users.api.serializers import UserSerializer


class MeAPIView(views.APIView):

    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)

        return response.Response(serializer.data, status=status.HTTP_200_OK)
