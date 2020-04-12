# from rest_framework import permissions
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
# from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
# from django.core import serializers

# from django.core.cache import cache


from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    # ListAPIView,
    RetrieveAPIView,
    # CreateAPIView,
    # DestroyAPIView,
    # UpdateAPIView
)

from .serializers import UserSerializer

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class UserDetails(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()