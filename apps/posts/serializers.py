from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from .models import (Post, Like, Bookmark)


class CommentSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations


    class Meta:
        model = Post
        fields =  '__all__'

class PostSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations
    # commentsDestails = CommentSerializer(read_only=True,many=True,)
    likesCount = serializers.IntegerField()
    # user =   serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # tagsCount = serializers.IntegerField()
    commentsCount = serializers.IntegerField()
    
    liked_or_not = serializers.SerializerMethodField()
    bookmarked_or_not = serializers.SerializerMethodField()
    # liked_or_not = serializers.BooleanField()

    class Meta:
        model = Post
        fields ='__all__'

    def get_liked_or_not(self, post, **kwargs):
        request = self.context.get('request')
        user = request.user

        return Like.objects.filter(post = post.post_id, user = user).exists()

    def get_bookmarked_or_not(self, post, **kwargs):
        request = self.context.get('request')
        user = request.user

        return Bookmark.objects.filter(post = post.post_id, user = user).exists()

    

            






    

    