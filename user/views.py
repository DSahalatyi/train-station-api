from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from user.schemas.user import create_user_view_schema, manage_user_view_schema
from user.serializers import UserSerializer


@create_user_view_schema
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


@manage_user_view_schema
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
