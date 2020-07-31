from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.db.models import OuterRef, Subquery, Count
import json

from guardian.shortcuts import remove_perm

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from django.core.cache import cache
import logging
# from stream_django.enrich import Enrich
from apps.friendship.models import (TimelineFeed, UserFeed, FollowersFeed)

# enricher = Enrich()
logger = logging.getLogger(__name__)




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
from .serializers import (PostSerializer, get_activity_serializer, 
        ActivitySerializer, CommentSerializer)
from apps.users.serializers import UserProfileSerializer




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
        post = Post.objects.get(post_id = postId)
        
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_posts(request, userId):
    """
    """
    try:
       
        posts = Post.objects.get(user = userId)
        data = PostSerializer(posts, many = True, context={'request': request}).data
       
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
def toggle_bookmark(request, postId):
    """
    """
    try:
       
        isBookmarked = request.data['isBookmarked']
        post = Post.objects.get(post_id = postId)
        if (isBookmarked):
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

        isDraft = True if data['isDraft'] == 'True' else False

        post = Post.objects.create(image=data['image'], description=data['description'],
                                    location=data['location'], privacy_type= data['privacyType'], is_draft = isDraft,
                                     user=request.user)
        # for user in data['nomineeList']:
        nomineeList = []
        for user in json.loads(data['nomineeList']):
            nomineeList.append(User.objects.get(username=user['username']))
           
        if nomineeList:
            post.nominees.add(*nomineeList)
        # post.save()    
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data ,status=status.HTTP_200_OK)
    except Exception as e:
        # logging.debug('Error')
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def modify_post(request, postId):
    # """
    # """
    try:
        data = request.data



        # user = User.objects.get(email = 'piyush.n.h@gmail.com')

        if not request.user.has_perm('posts.change_post', postId):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        post = Post.objects.get(post_id = postId)

        for k, v in data.items():
            setattr(post, k, v)
        post.save()
       
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def delete_post(request, postId):
    # """
    # """
    try:


        if not request.user.has_perm('posts.delete_post', postId):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        post = Post.objects.get(post_id = postId).delete()

       
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_timeline(request, pageSize, lastId='', ):
    # """
    # """
    try:
        # activities = FollowersFeed(request.user.user_id)[:]
        if lastId == 'null':
            data = TimelineFeed(request.user.user_id)[0:pageSize]
        else:
            data = TimelineFeed(request.user.user_id).filter(activity_id__lt=int(lastId))[0:pageSize]


        

        if len(data) < pageSize:
            hasMore = False
        elif len(data) == pageSize:
            hasMore = True

        if len(data) != 0:
            last_item_id = str(data[-1].serialization_id)
        else:
            last_item_id = lastId
            


       
        
        # activities = feed_manager.get_feed('timeline', request.user.user_id).get()['results']
        # enriched_activities = enricher.enrich_activities(activities)
        # data = []
        # for activity in enriched_activities:
        #      data.append(activity.activity_data)

        if len(data) > 1:
            serializer = ActivitySerializer(data,  context={'request': request}, many = True)
            responseData = serializer.data
        elif len(data) == 1:
            serializer = ActivitySerializer(data[0],  context={'request': request})
            responseData = [serializer.data]
        else:
            return Response([], status=status.HTTP_200_OK)

        return Response({'timeline': responseData, 'hasMore': hasMore, 'lastItemId': last_item_id} , status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def publish_comment(request, postId):
    
    try:
        data = request.data
        post = Post.objects.get(post_id = postId)
        comment = post.comments.create(comment_by=request.user, comment_type='text', text=data['text'])
        serializer = CommentSerializer(comment)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        # logging.debug('Error')
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def delete_comment(request, commentId):
    
    try:

        if not request.user.has_perm('posts.delete_comment', commentId):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        Comment.objects.get(comment_id = commentId).delete()

        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        logging.exception(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def modify_comment(request, commentId):
    # """
    # """
    try:
        data = request.data


        if not request.user.has_perm('posts.change_comment', commentId):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        comment = Post.objects.get(comment_id = commentId)

        for k, v in data.items():
            setattr(comment, k, v)
        comment.save()
       
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_post_comments(request, postId):
    """
    """
    try:
       
       
        comments = Post.objects.get(post_id = postId).comments
        
        serializer = CommentSerializer(comments, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)














