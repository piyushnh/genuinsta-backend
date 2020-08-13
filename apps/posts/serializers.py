from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from .models import (Post, Like, Bookmark, Comment)
from apps.users.serializers import UserProfileSerializer, UserSerializer

class LightPostSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations

    class Meta:
        model = Post
        fields =  ('image', 'pep', 'post_id')


class CommentSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations
    comment_by = UserSerializer(read_only = True)
    post = LightPostSerializer(read_only = True)

    class Meta:
        model = Comment
        fields =  '__all__'



class PostSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations
    # commentsDestails = CommentSerializer(read_only=True,many=True,)
    # user =   serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # tagsCount = serializers.IntegerField()
    comments = CommentSerializer(read_only=True,many=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user = UserProfileSerializer(read_only = True)
    
    username = serializers.CharField(source='user.username')
    firstname = serializers.CharField(source='user.first_name')
    surname = serializers.CharField(source='user.last_name')
    imgSrc = serializers.ImageField(source='image', use_url=True)

    liked_or_not = serializers.SerializerMethodField()
    filter = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    bookmarked_or_not = serializers.SerializerMethodField()
    # liked_or_not = serializers.BooleanField()
    # liked_or_not = serializers.BooleanField()

    class Meta:
        model = Post
        fields =('__all__')

    def get_filter(self, post, **kwargs):
        return ''

    def get_type(self, post, **kwargs):
        return 'user'
    def get_likes_count(self, post, **kwargs):
        return post.likes.count()

    def get_comments_count(self, post, **kwargs):
        return post.comments.count()

    def get_liked_or_not(self, post, **kwargs):
        request = self.context.get('request')
        user = request.user

        return Like.objects.filter(post = post.post_id, user = user).exists()

    def get_bookmarked_or_not(self, post, **kwargs):
        request = self.context.get('request')
        user = request.user

        return Bookmark.objects.filter(post = post.post_id, user = user).exists()

class LightPostSerializer(serializers.ModelSerializer):

        class Meta:
            model = Post
        fields =('image', 'post_id', )

class ActivitySerializer(serializers.Serializer):
    # id = serializers.UUIDField()
    # foreign_id = serializers.CharField()
    verb = serializers.CharField()
    time = serializers.DateTimeField()
    post = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_post(self, activity):
        post_id = activity.object_id
        post = Post.objects.get(post_id = post_id)
        return PostSerializer(post, context = self.context).data

    def get_user(self, activity):
        user_id = activity.actor_id
        user = User.objects.get(user_id = user_id)
        return UserProfileSerializer(user, context = self.context).data


    # def __init__(self, *args, **kwargs):
    #     object_serializer = kwargs.pop("object_serializer", None)
    #     actor_serializer = kwargs.pop("actor_serializer", None)
    #     # context = kwargs.pop("context", None)
    #     super().__init__(self, *args, **kwargs)
    #     if object_serializer:
    #         self.fields["object_temp"] = object_serializer(read_only=True)
    #     else:
    #         self.fields["object_temp"] = serializers.CharField()
    #     if actor_serializer:
    #         self.fields["actor"] = actor_serializer(read_only=True)
    #     else:
    #         self.fields["actor"] = serializers.CharField()

    class CommentSerializer(serializers.ModelSerializer):
   

        class Meta:
            model = Comment
            fields =('__all__')


    




class AggregatedSerializer(ActivitySerializer):
    group = serializers.CharField()
    activities = ActivitySerializer(many=True)


class NotificationSerializer(AggregatedSerializer):
    is_seen = serializers.BooleanField()
    is_read = serializers.BooleanField()


def get_activity_serializer(data, object_serializer=None, actor_serializer=None, context=None, **kwargs):
    kwargs["object_serializer"] = object_serializer
    kwargs["actor_serializer"] = actor_serializer
    serializer = ActivitySerializer
    if "is_seen" in data:
        serializer = NotificationSerializer
    elif "activities" in data:
        serializer = AggregatedSerializer
    return serializer(data, context = context, **kwargs)

    

            






    

    