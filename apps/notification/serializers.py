from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from .models import (Notification)
from apps.users.serializers import UserProfileSerializer, UserSerializer
from apps.posts.serializers import CommentSerializer, PostSerializer
from apps.posts.models import Comment, Post

class NotificationSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations

    class Meta:
        model = Notification
        fields =  '__all__'

class NotifActivitySerializer(serializers.Serializer):
    verb = serializers.CharField()
    time = serializers.DateTimeField()
    # notification = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()

    # def get_notification(self, activity):
    #     id = activity.object_id
    #     post = Post.objects.get(post_id = post_id)
    #     return PostSerializer(post, context = self.context).data

    def get_user(self, activity):
        user_id = activity.actor_id
        user = User.objects.get(user_id = user_id)
        return UserProfileSerializer(user, context = self.context).data

    def get_item(self, activity):
        verb_id = activity.verb.id
        object_id = activity.object_id
        if verb_id == 9 : #when commented
            comment = Comment.objects.get(comment_id = object_id).data
            return CommentSerializer(comment)
        if verb_id == 11 or verb_id == 12: #when recommend post or tag
            post = Post.objects.get(post_id = post_id)
            return PostSerializer(post, context=self.context).data
        if verb_id == 13: #when recommend pep
            pep = Pep.objects.get(id=object_id)
            return PepSerializer(pep).data
        
        return None



class AggregatedActivitySerializer(serializers.Serializer):
    is_read = serializers.BooleanField()
    is_seen = serializers.BooleanField()
    # time = serializers.DateTimeField()
    type = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    def get_type(self, activity):
        verb_dict = {
            7:'FRIEND_REQUEST_SENT',
            6:'FOLLOWED',
            8:'FRIEND_REQUEST_ACCEPTED',
            9:'COMMENTED'
        }
        return verb_dict[activity.verb.id]

    def get_activities(self, activity):
        
        return NotifActivitySerializer(activity.activities, many = True, context = self.context ).data
