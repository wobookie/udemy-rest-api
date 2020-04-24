from rest_framework import generics

from authentication.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    # Create a new authentication
    serializer_class = UserSerializer