from rest_framework import serializers
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from .models import (FriendshipRequest, Friend, Follow)

class FriendshipRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = FriendshipRequest
    fields = '__all__'

class FriendSerializer(serializers.ModelSerializer):
  class Meta:
    model = Friend
    fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
  class Meta:
    model = Follow
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
