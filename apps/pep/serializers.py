from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from .models import (Pep)
# from apps.users.serializers import UserProfileSerializer, UserSerializer

class PepSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations

    class Meta:
        model = Pep
        fields =  ('__all__')


