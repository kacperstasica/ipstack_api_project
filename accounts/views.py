from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from accounts.models import User
from accounts.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
