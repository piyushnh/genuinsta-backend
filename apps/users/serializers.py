from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from apps.friendship.models import Follow, Friend, FriendshipRequest

class AuthUserSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations
    firstname = serializers.CharField(source='first_name')
    surname = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ['username','firstname', 'surname', 'email',  'mobile_number' ]

class UserSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations


    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email',  'mobile_number' ]

class UserProfileSerializer(serializers.ModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     context = kwargs.get('context', None)
    #     if context:
    #         request = kwargs['context']['request']
    #         other_user = kwargs['context']['userId']
    #         other_user = User.objects.get(username = other_user)
    #         user = request.user
    #         print(str(other_user) + str(user))
    #         if user and other_user:
    #             try:
    #                 isFollowing  = Follow.objects.get(follower=user, followee = other_user)
    #             except :
    #                 isFollowing = None
    #             if isFollowing:
    #                 print(isFollowing)
    #                 self.fields['isFollowing'] = serializers.BooleanField(default=True)
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations
    FRIENDSHIP_CHOICES = [
        ('RS','REQUEST_SENT'),
        ('RR', 'REQUEST_RECEIVED'),
        ('AF','ARE_FRIENDS'),
        ('N','NONE')
    ]

    isFollowing = serializers.SerializerMethodField()
    friendshipStatus = serializers.SerializerMethodField()
    sentFriendRequestId = serializers.SerializerMethodField()
    receivedFriendRequestId = serializers.SerializerMethodField()
    # isFriendRequestReceived = serializers.BooleanField(default = False)
    # areFriends = serializers.BooleanField(default = False)
    firstname = serializers.CharField(source='first_name')
    surname = serializers.CharField(source='last_name')
    # profile_picture = serializers.SerializerMethodField()
 
    class Meta:
        model = User
        fields = ['firstname', 'surname', 'email',  'mobile_number', 'bio', 
                    'profile_picture', 'date_joined', 'isFollowing',
                    'friendshipStatus', 'username','sentFriendRequestId', 'receivedFriendRequestId' ]

    # def get_profile_picture(self, that_user, **kwargs):
    #     if that_user.profile_picture:
    #         return that_user.profile_picture
    #     elif that_user.profile_picture_url:
    #         return that_user.profile_picture_url

    def get_isFollowing(self, that_user, **kwargs):
        request = self.context.get('request')
        this_user = request.user
        

        return Follow.objects.follows(follower =  this_user, followee = that_user )

    def get_friendshipStatus(self, that_user, **kwargs):
        request = self.context.get('request')
        this_user = request.user
        

        return Friend.objects.friendship_status(this_user =  this_user, other_user = that_user )

    def get_sentFriendRequestId(self, that_user, **kwargs):
        request = self.context.get('request')
        this_user = request.user

        try:
            return FriendshipRequest.objects.get(from_user =  this_user, to_user = that_user ).id
        except:
            return ''

    def get_receivedFriendRequestId(self, that_user, **kwargs):
        request = self.context.get('request')
        this_user = request.user

        try:
            return FriendshipRequest.objects.get(from_user =  that_user, to_user = this_user ).id
        except:
            return ''


