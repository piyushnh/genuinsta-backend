from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.db.models import OuterRef, Subquery, Count

from django.core.cache import cache
import logging


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
    List all code snippets, or create a new snippet.
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
    List all code snippets, or create a new snippet.
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
    List all code snippets, or create a new snippet.
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
    List all code snippets, or create a new snippet.
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
    List all code snippets, or create a new snippet.
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

# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
# def publish_post(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     try:
       
       
       
#         return Response(status=status.HTTP_200_OK)
#     except Exception as e:
#         # logging.debug('Error')
#         print(e)
#         return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)






