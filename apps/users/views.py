# from rest_framework import permissions
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
# from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# from django.core import serializers

# from django.core.cache import cache

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    # ListAPIView,
    RetrieveAPIView,
    # CreateAPIView,
    # DestroyAPIView,
    # UpdateAPIView
)

#To integrate channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()

from .serializers import UserSerializer, UserProfileSerializer
from apps.friendship.models import Follow, Friend, FriendshipRequest

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None    

class UserDetails(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()

class UserProfile(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )
    
    def get_object(self):
        user_id = self.kwargs['userId']
        user = User.objects.get(username=user_id)

        return user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "userId": self.kwargs['userId']
            }
        )
        return context


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_profile(request, userId):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        async_to_sync(channel_layer.group_send)('random_group', {"type": "friend.request.received", 'request_data': 'hello'})

        this_user = request.user
        other_user = User.objects.get(user_id = userId)

        serialized_profile = UserProfileSerializer(other_user)
        # IMPORTANT to first assign it to a variable, coz modifying serialized_profile.data 
        # directly doesn't work
        data = serialized_profile.data

        isFollowing  = Follow.objects.follows(follower = this_user, followee = other_user)
       
        if isFollowing:
            data['isFollowing'] = True

        isFriendRequestSent = get_object_or_none(FriendshipRequest, from_user = this_user, to_user = other_user)
        isFriendRequestReceived = get_object_or_none(FriendshipRequest, from_user = other_user, to_user = this_user)
        
        if (not isFriendRequestSent) and (not isFriendRequestReceived):
            areFriends = Friend.objects.are_friends(this_user, other_user)  
        
        if isFriendRequestSent:
            data['friendshipStatus'] = 'REQUEST_SENT'
        elif isFriendRequestReceived:
            data['friendshipStatus'] = 'REQUEST_RECEIVED'
        elif areFriends:
            data['friendshipStatus'] = 'ARE_FRIENDS'
        else:
            data['friendshipStatus'] = 'NONE'
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
