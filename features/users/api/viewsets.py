from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from features.users.api.serializers import UserSerializer
from features.users.models import User

class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):

    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

    queryset = User.objects.all()
    
