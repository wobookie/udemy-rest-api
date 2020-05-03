from rest_framework import generics

from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    # Create a new users
    serializer_class = UserSerializer