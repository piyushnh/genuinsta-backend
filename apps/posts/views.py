from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.db.models import OuterRef, Subquery, Count

from guardian.shortcuts import remove_perm

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from django.core.cache import cache
import logging
from stream_django.feed_manager import feed_manager
# from .signals import *




from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)

from django.contrib.gis.geoip2 import GeoIP2
g = GeoIP2()

from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404

from . models import Post, Tag, Like, Comment, Bookmark
from .serializers import PostSerializer




@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_post(request, postId):
    """
    """
    try:
       
        # comments_count, likes_count, tags_count = get_post_counts(post)

        # comments = Comment.objects.filter(post_id=OuterRef('post_id'))
        # likes = Like.objects.filter(post_id=OuterRef('post_id'))
        # tags = Tags.objects.filter(post_id=OuterRef('post_id'))
        # commentsDetails = Subquery(comments.values('comment_id'))
        post = Post.objects.filter(post_id = postId).annotate( likesCount = Count('likes'), 
                            tagsCount = Count('tags'), commentsCount = Count('comments') )[0]
        print('hello')
        data = PostSerializer(post, context={'request': request}).data
       
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_posts(request, userId):
    """
    """
    try:
       
        posts = Post.objects.filter(user = userId).annotate( likesCount = Count('likes'), 
                            tagsCount = Count('tags'), commentsCount = Count('comments') )

        data = PostSerializer(posts, many = True, ontext={'request': request}).data
       
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_bookmarks(request, userId):
    """
    """
    try:
       
       
        post = Post.objects.filter(post_id__in = Bookmark.objects.filter(user__user_id = userId).values('post')).annotate( likesCount = Count('likes'), 
                             commentsCount = Count('comments') )
        data = PostSerializer(post, many=True, context={'request': request}).data
       
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        # logging.debug('Error')
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def like_unlike_post(request, postId):
    """
    """
    try:
       
        liked_or_not = request.data['likedOrNot']
        post = Post.objects.get(post_id = postId)
        if (liked_or_not):
            post.likes.get(user = request.user).delete()
        else:
            Like.objects.create(post = post, user = request.user)
       
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        # logging.debug('Error')
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def bookmark_unbookmark_post(request, postId):
    """
    """
    try:
       
        bookmarked_or_not = request.data['bookmarkedOrNot']
        post = Post.objects.get(post_id = postId)
        if (bookmarked_or_not):
            post.bookmarks.get(user = request.user).delete()
        else:
            Bookmark.objects.create(post = post, user = request.user)
       
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        # logging.debug('Error')
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#TODO: Implement get_post_likes 

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def publish_post(request):
    
    try:
        data = request.data

        Post.objects.create(data)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        # logging.debug('Error')
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def modify_post(request, postId):
    # """
    # """
    # try:
        # data = request.data



        # # user = User.objects.get(email = 'piyush.n.h@gmail.com')

        # if not request.user.has_perm('posts.change_post', postId):
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # post = Post.objects.get(post_id = postId)

        # for k, v in data.items():
        #     setattr(post, k, v)
        # post.save()

        print(feed_manager.get_user_feed(request.user.user_id))
        
       

        return Response(status=status.HTTP_200_OK)
    # except Exception as e:
    #     # logging.debug('Error')
    #     print(e)
    #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)







